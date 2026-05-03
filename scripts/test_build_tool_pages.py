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
