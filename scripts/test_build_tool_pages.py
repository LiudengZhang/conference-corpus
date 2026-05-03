"""Tests for the tool-dossier build pipeline added to build_site.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def test_tools_constant_loads():
    from build_site import TOOLS, INCLUSION_GATE
    assert isinstance(TOOLS, list)
    assert len(TOOLS) >= 15
    assert INCLUSION_GATE == 3
    # each row is (name, slug, family, aliases)
    for name, slug, family, aliases in TOOLS:
        assert isinstance(name, str) and name
        assert isinstance(slug, str) and slug.replace("-", "").isalnum()
        assert family in {"path-fm", "sc-fm", "spatial", "perturbation", "protein"}
        assert isinstance(aliases, list) and aliases


def test_match_aliases_word_boundary():
    from build_site import match_aliases
    text = "We applied scGPT and SC-GPT variants alongside Geneformer."
    aliases = ["scGPT", "SC-GPT"]
    assert match_aliases(text, aliases) is True


def test_match_aliases_negative_inside_word():
    from build_site import match_aliases
    # 'UCE' should not match inside 'reduces' or 'produces'
    text = "This reduces noise and produces clean embeddings."
    assert match_aliases(text, ["UCE"]) is False


def test_match_aliases_case_insensitive():
    from build_site import match_aliases
    assert match_aliases("we used cell2location to deconvolve", ["Cell2Location"]) is True


def test_load_corpus_dedups_posters():
    from build_site import load_corpus
    corpus = load_corpus()
    # poster Ids must be unique
    poster_ids = [p["Id"] for p in corpus["posters"]]
    assert len(poster_ids) == len(set(poster_ids))
    # session keys must be unique stems
    assert len(corpus["sessions"]) == len(set(s["stem"] for s in corpus["sessions"]))
    # corpus has substantial content
    assert len(corpus["posters"]) > 1500
    assert len(corpus["sessions"]) >= 20
    # every poster carries the topic-tracking fields
    for p in corpus["posters"]:
        assert "_topic" in p and isinstance(p["_topic"], str)
        assert "_topics" in p and isinstance(p["_topics"], list) and p["_topics"]
    # at least one poster surfaces in multiple topics (cross-topic dedup actually happened)
    assert any(len(p["_topics"]) > 1 for p in corpus["posters"])


def test_scan_mentions_returns_structured_hits():
    from build_site import load_corpus, scan_mentions
    corpus = load_corpus()
    # CHIEF should have at least one hit somewhere in the corpus
    hits = scan_mentions(corpus, ["CHIEF"])
    assert "posters" in hits and "sessions" in hits
    # Each hit has the fields the renderer needs
    if hits["posters"]:
        h = hits["posters"][0]
        assert "Id" in h and "Title" in h and "context" in h and "_topics" in h
    if hits["sessions"]:
        h = hits["sessions"][0]
        assert "stem" in h and "context" in h
