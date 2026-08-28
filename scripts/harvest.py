#!/usr/bin/env python3
"""Harvest the journal layer (L1) from PubMed E-utilities.

Writes one TSV per (month, domain) under the harvest directory:

    <harvest>/<YYYY-MM>/<domain>.tsv
    pmid <tab> sortpubdate <tab> journal <tab> "first .. last" <tab> title

This is the only route that can backfill. The RSS feeds listed in
data/sources.yml are a rolling window: once a month scrolls off, it is
gone, and no amount of re-polling brings it back.

Two things here are deliberate and should not be "simplified":

  * `journal article`[pt] with the review/editorial/news/comment/erratum/
    biography/case-report exclusions. Publication type is the only
    research-article filter that behaves consistently across publishers.
    OpenAlex `type:review` returns almost nothing for these journals, and
    reference-count heuristics collapse whole journals at a time.

  * `sortpubdate`, not the query month. PubMed `[dp]` matches *every*
    date on a record, so one paper is harvested two or three times, and
    Cell Press / JCO / Ann Oncol deposit records dated months into the
    future. The folder a row lands in is therefore the query month and
    is not to be trusted; build_index.py re-bins every row on this field.
    Harvest wide, bin later.

Usage:
    python3 scripts/harvest.py --from 2024-01 --to 2024-12 --harvest DIR
    python3 scripts/harvest.py --from 2026-08 --to 2026-08 --harvest DIR
"""

from __future__ import annotations

import argparse
import calendar
import json
import os
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ESEARCH = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
           "?db=pubmed&retmode=json&retmax=500&term=")
ESUMMARY = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            "?db=pubmed&retmode=json&id=")

RESEARCH = ('"journal article"[pt] NOT review[pt] NOT editorial[pt] '
            'NOT news[pt] NOT comment[pt] NOT "published erratum"[pt] '
            'NOT biography[pt] NOT "case reports"[pt]')

# The 33 journals of the corpus, by domain. Curated by tier, not by
# coverage: Cancer Discovery / Nature Cancer level and above. Cancer
# Research, Clinical Cancer Research and JNCI are deliberately absent.
JOURNALS = [
    ("general", "Nature"), ("general", "Science"), ("general", "Cell"),
    ("general", "N Engl J Med"), ("general", "Lancet"), ("general", "JAMA"),
    ("general", "Nat Med"), ("general", "Nat Genet"),
    ("cancer", "Cancer Discov"), ("cancer", "Nat Cancer"),
    ("cancer", "Cancer Cell"), ("cancer", "Lancet Oncol"),
    ("cancer", "J Clin Oncol"), ("cancer", "Ann Oncol"),
    ("cancer", "J Immunother Cancer"), ("cancer", "Blood"),
    ("immune", "Immunity"), ("immune", "Nat Immunol"),
    ("immune", "Sci Immunol"), ("immune", "J Exp Med"),
    ("immune", "Sci Transl Med"),
    ("bioinfo", "Nat Methods"), ("bioinfo", "Nat Biotechnol"),
    ("bioinfo", "Genome Biol"), ("bioinfo", "Genome Res"),
    ("bioinfo", "Bioinformatics"), ("bioinfo", "Nucleic Acids Res"),
    ("bioinfo", "Nat Comput Sci"), ("bioinfo", "Nat Mach Intell"),
    ("bioinfo", "Nat Biomed Eng"),
    ("sysbio", "Cell Syst"), ("sysbio", "Mol Syst Biol"),
    ("sysbio", "Cell Genom"),
]

PAUSE = 0.36  # NCBI allows 3 requests/sec without an API key


def get(url: str, tries: int = 5):
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(url, timeout=70))
        except Exception:
            time.sleep(1.6 * (i + 1))
    return None


def idlist(found) -> list[str] | None:
    """PMIDs from an esearch reply, or None if NCBI answered with an error.

    NCBI does not signal throttling with an HTTP status. It returns 200 and a
    body whose `esearchresult` carries an ERROR key and no `idlist` at all, so
    `found["esearchresult"]["idlist"]` raises KeyError partway through a run —
    which is how a 44-month harvest died on 2025-05 after four hours, having
    already written 29 months.

    None means "NCBI refused", which is not the same as "this journal-month is
    empty" and must not be recorded as an empty TSV. Distinguishing them is the
    whole point: an empty TSV is indistinguishable from a real gap, and the
    skip logic would then treat the month as done forever.
    """
    if not found:
        return None
    result = found.get("esearchresult") or {}
    if "idlist" not in result:
        return None
    return result["idlist"]


def months(start: str, end: str):
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    while (y, m) <= (ey, em):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def harvest_month(year: int, month: int, out: pathlib.Path) -> int:
    last = calendar.monthrange(year, month)[1]
    span = f'("{year}/{month:02d}/01"[dp] : "{year}/{month:02d}/{last}"[dp])'
    out.mkdir(parents=True, exist_ok=True)

    buckets: dict[str, list[str]] = {}
    for domain, journal in JOURNALS:
        found = get(ESEARCH + urllib.parse.quote(
            f'"{journal}"[ta] AND {span} AND {RESEARCH}'))
        ids = idlist(found)
        if ids is None:
            # Back off hard and retry once. If NCBI still refuses, abandon the
            # whole month rather than write a TSV missing this journal — a
            # partial month looks complete to the skip logic on the next run.
            time.sleep(20)
            ids = idlist(get(ESEARCH + urllib.parse.quote(
                f'"{journal}"[ta] AND {span} AND {RESEARCH}')))
        if ids is None:
            print(f"  {year}-{month:02d}: NCBI refused for {journal}; "
                  f"month abandoned, nothing written", flush=True)
            return -1
        time.sleep(PAUSE)

        rows = []
        for i in range(0, len(ids), 200):
            summary = get(ESUMMARY + ",".join(ids[i:i + 200]))
            time.sleep(PAUSE)
            if not summary:
                continue
            result = summary.get("result", {})
            for pmid in result.get("uids", []):
                rec = result[pmid]
                title = re.sub(r"<[^>]+>", "", rec.get("title", "")).strip().rstrip(".")
                first = rec.get("sortfirstauthor", "") or "?"
                authors = rec.get("authors") or [{}]
                lastau = authors[-1].get("name", "?")
                rows.append("\t".join([
                    pmid, rec.get("sortpubdate", "")[:10], journal,
                    f"{first} .. {lastau}", title,
                ]))
        buckets.setdefault(domain, []).extend(rows)

    total = 0
    for domain, rows in buckets.items():
        (out / f"{domain}.tsv").write_text("\n".join(rows), encoding="utf-8")
        total += len(rows)
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", required=True, help="YYYY-MM")
    ap.add_argument("--to", dest="end", required=True, help="YYYY-MM")
    ap.add_argument("--harvest", default=os.environ.get("HARVEST", ""),
                    help="directory to write <month>/<domain>.tsv into")
    ap.add_argument("--force", action="store_true",
                    help="re-pull months that already have TSVs")
    args = ap.parse_args()
    if not args.harvest:
        sys.exit("give --harvest DIR (or set HARVEST)")
    root = pathlib.Path(args.harvest)

    grand = 0
    refused: list[str] = []
    for year, month in months(args.start, args.end):
        out = root / f"{year}-{month:02d}"
        if out.is_dir() and any(out.glob("*.tsv")) and not args.force:
            print(f"{year}-{month:02d}: already harvested, skipping", flush=True)
            continue
        n = harvest_month(year, month, out)
        if n < 0:
            # Abandoned, not empty. Leave the (empty) directory so the skip
            # test — which looks for TSVs, not for the directory — re-tries it
            # on the next run, and keep going: one refused month should not
            # cost the 15 that come after it.
            refused.append(f"{year}-{month:02d}")
            continue
        grand += n
        print(f"{year}-{month:02d}: {n:,} articles -> {out}", flush=True)
    print(f"GRAND TOTAL {grand:,}")
    if refused:
        print(f"REFUSED, re-run to pick up: {', '.join(refused)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
