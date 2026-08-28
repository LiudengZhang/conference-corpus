#!/usr/bin/env python3
"""Harvest PubMed abstracts for the title-floor measurement.

The journal layer (data/index.sqlite) stores titles only. Every 2023 evidence
card was therefore written against a title and a journal name, and every 2023
briefing says so. This script pulls the abstracts needed to measure what that
costs, into a regenerable data/abstracts.sqlite.

Two arms, and the control is the point:

  arm A  every distinct PMID cited in docs/briefings/*.md plus every PMID in
         data/evidence.yml (card pmids and their `companions`). Reading these
         can show cards that were misjudged. It can never show a paper a title
         hid, because a hidden paper was never carded.

  arm B  the control. A seeded random sample of 2023 papers from
         data/index.sqlite that were never carded and never cited, stratified
         across the five domains in proportion to their 2023 volume. This is
         the only arm that can measure omission.

THE TRAP (see scripts/harvest.py `idlist`): NCBI does not signal throttling
with an HTTP status. It answers 200 with a body carrying an error and no
payload. A naive parser records "this batch has no abstracts" — an absence —
where the truth is "NCBI refused". Absence is sticky: the resume logic then
skips those PMIDs forever. So `fetch_batch` returns None for refusal and a
(possibly partial) dict for success, and only success is ever written. A PMID
that came back with no <Abstract> element at all is written with
status='no-abstract'; a PMID nobody answered for is simply not written, and
the next run picks it up.

Usage:
    python3 scripts/harvest_abstracts.py --plan          # build both arms
    python3 scripts/harvest_abstracts.py --fetch         # harvest, resumable
    python3 scripts/harvest_abstracts.py --status
"""

from __future__ import annotations

import argparse
import pathlib
import random
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "index.sqlite"
EVIDENCE = ROOT / "data" / "evidence.yml"
BRIEFINGS = ROOT / "docs" / "briefings"
OUT = ROOT / "data" / "abstracts.sqlite"

EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
UA = "conference-corpus/1.0 (mailto:liudengzhang91@gmail.com)"
PAUSE = 0.36  # NCBI allows 3 requests/sec without an API key
BATCH = 150

DOMAINS = ["general", "bioinfo", "cancer", "immune", "sysbio"]


# ---------------------------------------------------------------- storage

def connect() -> sqlite3.Connection:
    db = sqlite3.connect(OUT)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
        CREATE TABLE IF NOT EXISTS wanted(
            pmid TEXT PRIMARY KEY, arm TEXT, domain TEXT, month TEXT,
            journal TEXT, title TEXT);
        CREATE TABLE IF NOT EXISTS abstracts(
            pmid TEXT PRIMARY KEY, arm TEXT, journal TEXT, pubdate TEXT,
            title TEXT, abstract TEXT, pubtypes TEXT, status TEXT,
            fetched_at TEXT);
        CREATE INDEX IF NOT EXISTS i_arm ON wanted(arm);
        CREATE INDEX IF NOT EXISTS i_aarm ON abstracts(arm);
        """
    )
    return db


# ---------------------------------------------------------------- arm sets

def briefing_pmids() -> set[str]:
    pm: set[str] = set()
    for f in sorted(BRIEFINGS.glob("*.md")):
        pm |= set(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,9})",
                             f.read_text(encoding="utf-8")))
    return pm


def evidence_pmids() -> tuple[set[str], set[str]]:
    txt = EVIDENCE.read_text(encoding="utf-8")
    cards = set(re.findall(r"\n\s*pmid:\s*\"?(\d{7,9})\"?", txt))
    comps: set[str] = set()
    for grp in re.findall(r"companions:\s*\[(.*?)\]", txt, re.S):
        comps |= set(re.findall(r"\d{7,9}", grp))
    return cards, comps


def plan(db: sqlite3.Connection, seed: int, n_b: int) -> None:
    brief = briefing_pmids()
    cards, comps = evidence_pmids()
    arm_a = brief | cards | comps
    print(f"arm A: {len(brief)} cited in briefings, {len(cards)} card pmids, "
          f"{len(comps)} companions -> {len(arm_a)} distinct")

    idx = sqlite3.connect(f"file:{INDEX}?mode=ro", uri=True)
    meta = {p: (d, m, j, t) for p, d, m, j, t in idx.execute(
        "SELECT pmid, domain, month, journal, title FROM papers")}

    rows = [(p, "A", meta.get(p, (None,))[0],
             meta.get(p, (None, None))[1] if p in meta else None,
             meta[p][2] if p in meta else None,
             meta[p][3] if p in meta else None) for p in sorted(arm_a)]
    db.executemany("INSERT OR IGNORE INTO wanted VALUES(?,?,?,?,?,?)", rows)

    # arm B: 2023 papers never carded and never cited, stratified by domain.
    pool: dict[str, list[tuple]] = {d: [] for d in DOMAINS}
    for pmid, (dom, month, jrnl, title) in meta.items():
        if month and month.startswith("2023-") and pmid not in arm_a:
            pool.setdefault(dom, []).append((pmid, dom, month, jrnl, title))

    sizes = {d: len(pool.get(d, [])) for d in DOMAINS}
    total = sum(sizes.values())
    quota: dict[str, int] = {}
    rema: list[tuple[float, str]] = []
    for d in DOMAINS:
        exact = sizes[d] / total * n_b
        quota[d] = int(exact)
        rema.append((exact - int(exact), d))
    for _, d in sorted(rema, reverse=True)[:n_b - sum(quota.values())]:
        quota[d] += 1
    print(f"arm B pool (2023, un-carded, un-cited): {total}; quota {quota}")

    rng = random.Random(seed)
    brows = []
    for d in DOMAINS:
        cand = sorted(pool.get(d, []))
        for pmid, dom, month, jrnl, title in rng.sample(cand, quota[d]):
            brows.append((pmid, "B", dom, month, jrnl, title))
    db.executemany("INSERT OR IGNORE INTO wanted VALUES(?,?,?,?,?,?)", brows)

    db.execute("INSERT OR REPLACE INTO meta VALUES('seed',?)", (str(seed),))
    db.execute("INSERT OR REPLACE INTO meta VALUES('arm_b_n',?)", (str(n_b),))
    db.execute("INSERT OR REPLACE INTO meta VALUES('arm_b_quota',?)",
               (repr(quota),))
    db.execute("INSERT OR REPLACE INTO meta VALUES('arm_b_pool',?)",
               (repr(sizes),))
    db.commit()
    print(f"planned: {len(rows)} arm A + {len(brows)} arm B")


# ---------------------------------------------------------------- fetching

class Refused(Exception):
    """NCBI answered, but with an error or an empty payload."""


def http(pmids: list[str], tries: int = 6) -> str:
    body = urllib.parse.urlencode({
        "db": "pubmed", "rettype": "abstract", "retmode": "xml",
        "id": ",".join(pmids)}).encode()
    last = ""
    for i in range(tries):
        try:
            req = urllib.request.Request(
                EFETCH, data=body, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - retry everything
            last = repr(exc)
            time.sleep(1.6 * (i + 1) ** 2)
    raise Refused(f"transport gave up: {last}")


def text_of(node) -> str:
    """Flatten a node's text, keeping structured-abstract labels."""
    parts = []
    for ab in node:
        label = ab.get("Label")
        body = "".join(ab.itertext()).strip()
        if not body:
            continue
        parts.append(f"{label}: {body}" if label else body)
    return "\n".join(parts)


def parse(xml: str, asked: list[str]) -> dict[str, dict]:
    """Records keyed by pmid, or raise Refused.

    An <ERROR> body, unparseable XML, or zero articles for a non-empty ask are
    all refusals, not emptiness. A batch that returns some articles is trusted
    for those; the rest stay unwritten and are re-asked on the next run.
    """
    if "<ERROR>" in xml or "<error>" in xml:
        raise Refused(xml[:200])
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise Refused(f"unparseable: {exc}") from exc

    out: dict[str, dict] = {}
    for art in root.iter("PubmedArticle"):
        pmid_el = art.find("./MedlineCitation/PMID")
        if pmid_el is None or not pmid_el.text:
            continue
        pmid = pmid_el.text.strip()
        art_el = art.find("./MedlineCitation/Article")
        title = ""
        if art_el is not None:
            t = art_el.find("ArticleTitle")
            if t is not None:
                title = "".join(t.itertext()).strip()
        jrnl = art.findtext("./MedlineCitation/Article/Journal/ISOAbbreviation") or ""
        y = art.findtext("./MedlineCitation/Article/Journal/JournalIssue/PubDate/Year") or ""
        mo = art.findtext("./MedlineCitation/Article/Journal/JournalIssue/PubDate/Month") or ""
        ab_el = art.find("./MedlineCitation/Article/Abstract")
        abstract = text_of(ab_el) if ab_el is not None else ""
        pts = ";".join(
            (e.text or "") for e in art.iter("PublicationType"))
        out[pmid] = {
            "title": title, "journal": jrnl, "pubdate": f"{y} {mo}".strip(),
            "abstract": abstract, "pubtypes": pts,
            "status": "ok" if abstract else "no-abstract",
        }
    if asked and not out:
        raise Refused("200 with zero PubmedArticle elements")
    return out


def fetch(db: sqlite3.Connection, arm: str | None, limit: int | None) -> int:
    q = ("SELECT pmid, arm FROM wanted WHERE pmid NOT IN "
         "(SELECT pmid FROM abstracts)")
    if arm:
        q += f" AND arm='{arm}'"
    q += " ORDER BY arm, pmid"
    todo = db.execute(q).fetchall()
    if limit:
        todo = todo[:limit]
    print(f"{len(todo)} pmids outstanding")

    armof = dict(todo)
    written = 0
    for i in range(0, len(todo), BATCH):
        chunk = [p for p, _ in todo[i:i + BATCH]]
        for attempt in range(3):
            try:
                recs = parse(http(chunk), chunk)
                break
            except Refused as exc:
                wait = 30 * (attempt + 1)
                print(f"  REFUSED ({exc}); backing off {wait}s", flush=True)
                time.sleep(wait)
        else:
            print("  NCBI still refusing; stopping. Re-run to resume.",
                  flush=True)
            db.commit()
            return written
        now = time.strftime("%Y-%m-%dT%H:%M:%S")
        db.executemany(
            "INSERT OR REPLACE INTO abstracts VALUES(?,?,?,?,?,?,?,?,?)",
            [(p, armof.get(p, "?"), r["journal"], r["pubdate"], r["title"],
              r["abstract"], r["pubtypes"], r["status"], now)
             for p, r in recs.items()])
        db.commit()
        written += len(recs)
        missing = len(chunk) - len(recs)
        print(f"  [{i + len(chunk)}/{len(todo)}] +{len(recs)}"
              + (f" ({missing} unanswered, will retry)" if missing else ""),
              flush=True)
        time.sleep(PAUSE)
    return written


def status(db: sqlite3.Connection) -> None:
    for k, v in db.execute("SELECT k, v FROM meta"):
        print(f"{k} = {v}")
    for arm, n in db.execute("SELECT arm, count(*) FROM wanted GROUP BY arm"):
        got = db.execute(
            "SELECT count(*) FROM abstracts WHERE arm=?", (arm,)).fetchone()[0]
        ok = db.execute(
            "SELECT count(*) FROM abstracts WHERE arm=? AND status='ok'",
            (arm,)).fetchone()[0]
        print(f"arm {arm}: wanted {n}, fetched {got}, with abstract {ok}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", action="store_true",
                    help="compute both arms into the wanted table")
    ap.add_argument("--fetch", action="store_true", help="harvest, resumable")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--arm", choices=["A", "B", "C"], help="restrict --fetch")
    ap.add_argument("--limit", type=int, help="stop after N pmids")
    ap.add_argument("--seed", type=int, default=20230101,
                    help="RNG seed for the arm B sample (recorded in meta)")
    ap.add_argument("--arm-b-n", type=int, default=300)
    args = ap.parse_args()
    if not (args.plan or args.fetch or args.status):
        ap.error("give --plan, --fetch or --status")

    db = connect()
    if args.plan:
        plan(db, args.seed, args.arm_b_n)
    if args.fetch:
        n = fetch(db, args.arm, args.limit)
        print(f"wrote {n} records")
    if args.status or args.plan or args.fetch:
        status(db)
    return 0


if __name__ == "__main__":
    sys.exit(main())
