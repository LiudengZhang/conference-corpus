#!/usr/bin/env python3
"""Build the interactive supplementary figures for the FM-to-Virtual-Cells talk.

Companion to scripts/fm_citation_plot.py — same Plotly conventions (self-contained
HTML, plotly.js from CDN), but these figures carry the arguments the talk
otherwise asks the audience to hold in their head.

Outputs (all → docs/talks/assets/):
  fm-reckoning-corpus.html        — §1.3  the 2025 reckoning becomes a 12-paper corpus
  fm-lineage-tree.html            — §1.3  NLP origin → reckoning → 2026 architectural response
  fm-lanes-map.html               — §3.1  the 9 application lanes, cost vs time-to-result
  fm-compute-landscape.html       — Act 2  params vs training cost, and the linear baseline
  agentic-fm-patterns.html        — agentic-meets-foundation explainer: the four patterns
  fm-four-causes.html             — why-linear-baselines-win: four overlapping causes
  fm-cause-track-matrix.html      — why-linear-baselines-win: cause × small-lab-track matrix
  fm-arc-timeline.html            — §1.3  the 2023–2026 arc as three interleaved swimlanes
  fm-eval-catalog-timeline.html   — evaluation-papers-catalog: corpus by venue tier
  fm-institutional-landscape.html — §2.2  institutes by build activity vs critique activity

The data below is hardcoded with inline source tags — these are small,
figure-specific tables curated from the talk's own supplementary resources
matrix and evaluation-papers catalog, not external feeds. Re-run by hand when
those source pages change.

Usage:
    python scripts/fm_talk_figures.py
"""

from __future__ import annotations

import datetime as dt
import math
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "docs/talks/assets"

PLOTLY_CONFIG = {"responsive": True, "displaylogo": False}


def write_fig(fig: go.Figure, name: str) -> None:
    out_path = ASSETS / name
    fig.write_html(
        out_path,
        include_plotlyjs="cdn",
        full_html=True,
        config=PLOTLY_CONFIG,
    )
    print(f"  → wrote {out_path.relative_to(REPO_ROOT)}")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1 — the reckoning becomes a corpus
# Source: docs/talks/fm-to-virtual-cells/evaluation-papers-catalog.md
# ─────────────────────────────────────────────────────────────────────────────

RECKONING = [
    dict(name="Csendes scPerturBench", date="2024-09", venue="BM2 Lab preprint",
         axis="replication",
         headline="Original scGPT train/test split was leaky; clean splits expose failure",
         models="scGPT replication"),
    dict(name="Kedzierska et al.", date="2025-04", venue="Genome Biology",
         axis="perturbation",
         headline="scFMs lose to PCA + kNN in the zero-shot setting",
         models="scGPT, Geneformer, UCE, scFoundation"),
    dict(name="Wenkel et al.", date="2025-07", venue="Nature Methods",
         axis="perturbation",
         headline="latent-additive + scGPT-embeddings is the new baseline floor",
         models="sc-FMs vs latent-additive"),
    dict(name="PertEval-scFM", date="2025-07", venue="ICML 2025",
         axis="perturbation",
         headline="Most scFM embeddings don't beat baselines on strong/atypical perturbations",
         models="scFM embeddings, standardized framework"),
    dict(name="Ahlmann-Eltze & Huber", date="2025-08", venue="Nature Methods",
         axis="perturbation",
         headline="No sc-FM beats the mean-of-training-perturbations linear baseline (<$2k compute)",
         models="6 sc-FMs (scGPT, Geneformer, scFoundation, GEARS, CPA) + UCE"),
    dict(name="Wu et al. (Genome Biology)", date="2025-10", venue="Genome Biology",
         axis="beyond-perturbation",
         headline="No single scFM consistently outperforms others across tasks",
         models="6 scFMs, cell-ontology-grounded metrics"),
    dict(name="Wu et al. (Nat Methods)", date="2026-01", venue="Nature Methods",
         axis="perturbation",
         headline="Axis-by-axis failure decomposition — 27 methods × 29 datasets × 6 metrics",
         models="27 methods"),
    dict(name="Liu et al. (scEval)", date="2026-01", venue="Advanced Science",
         axis="beyond-perturbation",
         headline="Challenges the necessity of developing FMs for single-cell analysis",
         models="10 scFMs × 8 tasks"),
    dict(name="Parameter-free baseline", date="2026-02", venue="bioRxiv",
         axis="perturbation",
         headline="Parameter-free representations win on downstream benchmarks",
         models="sc-FMs vs parameter-free reps"),
    dict(name="Cellular-dynamics zero-shot", date="2026-03", venue="bioRxiv",
         axis="new-dimension",
         headline="zero-shot scFMs fail to recover RNA-velocity / cellular dynamics",
         models="zero-shot scFM embeddings"),
    dict(name="CellBench-LS", date="2026-04", venue="bioRxiv",
         axis="beyond-perturbation",
         headline="Low-supervision: FMs lead cell-type, classical leads gene-expression",
         models="7 scFMs + PCA / UMAP / scVI"),
    dict(name="Han et al. (real-world)", date="2026-04", venue="bioRxiv",
         axis="new-dimension",
         headline="Industry-grade robustness gaps in real-world data integration",
         models="scFMs in pharma deployment"),
]

CONTRARIAN = dict(
    name="FMs Improve Perturbation Response Prediction", date="2026-02",
    venue="bioRxiv",
    headline="With sufficient data, FMs DO improve genetic + chemical perturbation prediction",
    models="sc-FMs trained with sufficient data",
)

AXIS_COLOR = {
    "perturbation": "#d62728",
    "beyond-perturbation": "#9467bd",
    "new-dimension": "#1f77b4",
    "replication": "#7f7f7f",
}
AXIS_LABEL = {
    "perturbation": "Perturbation prediction — the original reckoning",
    "beyond-perturbation": "Beyond perturbation — most cell-level tasks",
    "new-dimension": "New evaluation dimensions",
    "replication": "Replication + clean splits",
}


def _ts(ym: str) -> pd.Timestamp:
    return pd.Timestamp(ym + "-01")


def build_reckoning_corpus() -> None:
    rows = sorted(RECKONING, key=lambda r: r["date"])
    for i, r in enumerate(rows, start=1):
        r["cum"] = i
        r["ts"] = _ts(r["date"])

    fig = go.Figure()

    # Cumulative step line through every reckoning paper.
    fig.add_trace(
        go.Scatter(
            x=[r["ts"] for r in rows],
            y=[r["cum"] for r in rows],
            mode="lines",
            line=dict(shape="hv", color="#999", width=2),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # One marker trace per evaluation axis so the legend reads by axis.
    for axis, color in AXIS_COLOR.items():
        sub = [r for r in rows if r["axis"] == axis]
        if not sub:
            continue
        fig.add_trace(
            go.Scatter(
                x=[r["ts"] for r in sub],
                y=[r["cum"] for r in sub],
                mode="markers",
                name=AXIS_LABEL[axis],
                marker=dict(size=15, color=color, line=dict(color="#fff", width=1.5)),
                customdata=[
                    [r["name"], r["venue"], r["date"], r["headline"], r["models"]]
                    for r in sub
                ],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "%{customdata[1]} · %{customdata[2]}<br>"
                    "Models: %{customdata[4]}<br>"
                    "<i>%{customdata[3]}</i>"
                    "<extra></extra>"
                ),
            )
        )

    # The contrarian voice — deliberately off the corpus, below the axis.
    fig.add_trace(
        go.Scatter(
            x=[_ts(CONTRARIAN["date"])],
            y=[-0.9],
            mode="markers",
            name="The contrarian voice",
            marker=dict(size=17, color="#2ca02c", symbol="x",
                        line=dict(color="#1a661a", width=1)),
            customdata=[[CONTRARIAN["name"], CONTRARIAN["venue"],
                         CONTRARIAN["date"], CONTRARIAN["headline"],
                         CONTRARIAN["models"]]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]} · %{customdata[2]}<br>"
                "Models: %{customdata[4]}<br>"
                "<i>%{customdata[3]}</i>"
                "<extra></extra>"
            ),
        )
    )

    # Call out the canonical blow.
    ae = next(r for r in rows if r["name"].startswith("Ahlmann-Eltze"))
    fig.add_annotation(
        x=ae["ts"], y=ae["cum"],
        text="Aug 2025 — the canonical blow",
        showarrow=True, arrowhead=2, arrowcolor="#888",
        ax=-55, ay=-38, font=dict(size=10, color="#555"),
    )
    fig.add_annotation(
        x=_ts(CONTRARIAN["date"]), y=-0.9,
        text="Contrarian: with enough data, FMs <i>do</i> improve —<br>"
             "the reckoning is contested, not closed",
        showarrow=True, arrowhead=2, arrowcolor="#2ca02c",
        ax=-10, ay=-58, font=dict(size=10, color="#2a7a2a"),
        align="center",
    )

    fig.update_layout(
        title=dict(
            text=(
                "The 2025 reckoning becomes a corpus<br>"
                "<sub>12 single-cell-FM evaluation papers, 2024–2026 — by Apr 2026 "
                "a discipline-wide consensus, then a contested one.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(title="Publication date", gridcolor="#e6e6e6",
                   range=["2024-06-01", "2026-06-01"]),
        yaxis=dict(title="Cumulative reckoning papers", gridcolor="#e6e6e6",
                   range=[-1.6, 13], dtick=2),
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
        legend=dict(title="Evaluation axis", bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#bbb", borderwidth=1,
                    x=0.02, xanchor="left", y=0.98, yanchor="top"),
        margin=dict(l=70, r=40, t=80, b=60),
        height=540,
    )
    write_fig(fig, "fm-reckoning-corpus.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2 — the 9 application lanes, cost vs time-to-result
# Source: docs/talks/fm-to-virtual-cells.md §3.1
# ─────────────────────────────────────────────────────────────────────────────

LANES = [
    dict(n=1, name="FM embeddings as features", cost_lo=100, cost_hi=500,
         mo_lo=0.5, mo_hi=1.5, risk="low",
         summary="Frozen UNI2-h / scGPT embeddings → attention-MIL → clinical readout.",
         win="Clinical relevance at zero pretraining cost."),
    dict(n=2, name="PEFT / LoRA / adapters", cost_lo=500, cost_hi=5000,
         mo_lo=2, mo_hi=4, risk="medium",
         summary="<1% trainable adapter on a frozen scGPT / Geneformer / UNI2 backbone.",
         win="Zero-shot generalization to unseen drugs and cell lines."),
    dict(n=3, name="Domain-specific small FM", cost_lo=10000, cost_hi=50000,
         mo_lo=6, mo_hi=12, risk="medium-high",
         summary="Continual-pretrain a smaller model on your domain corpus.",
         win="Domain curation beats scale — Geneformer V2-104M_CLcancer."),
    dict(n=4, name="Negative results / replication", cost_lo=100, cost_hi=2000,
         mo_lo=3, mo_hi=6, risk="low",
         summary="Replicate a published FM claim against a linear baseline.",
         win="Most-published lane of 2025–2026; target an uncovered axis."),
    dict(n=5, name="Benchmark / dataset curation", cost_lo=100, cost_hi=5000,
         mo_lo=6, mo_hi=18, risk="low",
         summary="Curate a held-out split or new benchmark dataset.",
         win="Your dataset becomes infrastructure every model cites."),
    dict(n=6, name="FM-wrapper tools / pipelines", cost_lo=100, cost_hi=5000,
         mo_lo=6, mo_hi=12, risk="low",
         summary="Wrap a popular FM in a Bioconductor / scverse / browser-native tool.",
         win="Adoption-driven citations."),
    dict(n=7, name="FM-aided wet-lab / clinical study", cost_lo=5000, cost_hi=50000,
         mo_lo=12, mo_hi=24, risk="low",
         summary="Use a frozen FM as instrumentation in a clinical or wet-lab study.",
         win="Janowczyk 2025 Nat Med — first deployment-grade exemplar."),
    dict(n=8, name="FM as generative data-augmentation engine",
         cost_lo=100, cost_hi=2000, mo_lo=3, mo_hi=6, risk="medium",
         summary="Use a generative FM to synthesize labeled training cells for rare cohorts.",
         win="xVERSE resolves rare cell types with as few as 4 cells."),
    dict(n=9, name="FM-aided experimental design / active learning",
         cost_lo=1000, cost_hi=10000, mo_lo=12, mo_hi=18, risk="medium",
         summary="FM-guided experimental-design loop with a wet-lab partner.",
         win="The pattern AI-native biotechs actually pay for."),
]

RISK_COLOR = {"low": "#2ca02c", "medium": "#ff7f0e", "medium-high": "#d62728"}


def build_lanes_map() -> None:
    fig = go.Figure()

    for risk, color in RISK_COLOR.items():
        sub = [l for l in LANES if l["risk"] == risk]
        if not sub:
            continue
        xs = [math.sqrt(l["cost_lo"] * l["cost_hi"]) for l in sub]
        ys = [(l["mo_lo"] + l["mo_hi"]) / 2 for l in sub]
        fig.add_trace(
            go.Scatter(
                x=xs, y=ys,
                mode="markers+text",
                name=f"{risk} risk",
                text=[f"L{l['n']}" for l in sub],
                textposition="middle center",
                textfont=dict(size=11, color="white"),
                marker=dict(size=40, color=color, opacity=0.85,
                            line=dict(color="#333", width=1)),
                error_x=dict(
                    type="data", symmetric=False,
                    array=[l["cost_hi"] - x for l, x in zip(sub, xs)],
                    arrayminus=[x - l["cost_lo"] for l, x in zip(sub, xs)],
                    color=color, thickness=1, width=4,
                ),
                customdata=[
                    [l["name"], f"${l['cost_lo']:,}–${l['cost_hi']:,}",
                     f"{l['mo_lo']:g}–{l['mo_hi']:g}", l["risk"],
                     l["summary"], l["win"]]
                    for l in sub
                ],
                hovertemplate=(
                    "<b>Lane %{text}: %{customdata[0]}</b><br>"
                    "Typical cost: %{customdata[1]}<br>"
                    "Months to first result: %{customdata[2]}<br>"
                    "Risk: %{customdata[3]}<br>"
                    "%{customdata[4]}<br>"
                    "<i>Win: %{customdata[5]}</i>"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=dict(
            text=(
                "The 9 application lanes — cost vs time-to-first-result<br>"
                "<sub>Bubble = lane; horizontal bars = the typical cost range; "
                "colour = project risk. Hover for the one-line summary and the win.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(title="Typical project cost, USD (log scale)", type="log",
                   gridcolor="#e6e6e6", range=[math.log10(70), math.log10(90000)]),
        yaxis=dict(title="Months to first result", gridcolor="#e6e6e6",
                   range=[-1, 26]),
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
        legend=dict(title="Project risk", bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#bbb", borderwidth=1,
                    x=0.98, xanchor="right", y=0.98, yanchor="top"),
        margin=dict(l=70, r=40, t=80, b=60),
        height=540,
    )
    write_fig(fig, "fm-lanes-map.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3 — FM lineage: NLP origin → reckoning → 2026 response
# Source: docs/talks/fm-to-virtual-cells.md §1.3 +
#         docs/talks/fm-to-virtual-cells/why-linear-baselines-win.md
# ─────────────────────────────────────────────────────────────────────────────

GEN1 = [
    ("scGPT", "Next-gene-prediction transformer; 51M params. The reckoning's most-evaluated target."),
    ("Geneformer", "Masked-gene-modelling transformer; the other canonical sc-FM."),
    ("UCE", "Universal Cell Embedding; 650M params, largest published sc-FM."),
    ("scFoundation", "Read-depth-aware attention — closest Gen-1 model to architecture–biology co-design."),
    ("CellPLM", "Cell-language pretraining; included in most 2026 evaluation sweeps."),
]
GEN2 = [
    ("xVERSE", "cause2",
     "Transcriptomics-native (non-LM) architecture; +17.9% representation, +34.3% spatial imputation over LM-derived sc-FMs."),
    ("TxPert", "cause2",
     "Multiple knowledge graphs as the perturbation-prediction inductive bias — Wenkel co-authored the latent-additive critique: the reckoning answering itself."),
    ("TranscriptFormer", "cause2",
     "Generative cross-species architecture; 112M cells × 12 species × 1.53B years of evolution."),
    ("Compositional FMs (Theis)", "cause2",
     "Stop training monolithic sc-FMs; compose modality-specific FMs instead."),
    ("Causal-objective pretraining", "cause1",
     "Counterfactual / IRM / contrastive-perturbation losses that target causality rather than correlation (Track 2)."),
]

CAUSE_COLOR = {"cause1": "#1f77b4", "cause2": "#ff7f0e"}
CAUSE_LABEL = {
    "cause1": "fixes Cause 1 — a causal training objective",
    "cause2": "fixes Cause 2 — a biology-native architecture",
}


def build_lineage_tree() -> None:
    x_origin, x_gen1, x_reck, x_gen2 = 0.0, 1.0, 2.0, 3.0

    def spread(n: int) -> list[float]:
        if n == 1:
            return [0.0]
        return [2.0 - 4.0 * i / (n - 1) for i in range(n)]

    gen1_y = spread(len(GEN1))
    gen2_y = spread(len(GEN2))
    origin_pos = (x_origin, 0.0)
    reck_pos = (x_reck, 0.0)

    fig = go.Figure()

    # ── edges ────────────────────────────────────────────────────────────
    # NLP origin → each Gen-1 model (structural inheritance).
    ex, ey = [], []
    for y in gen1_y:
        ex += [x_origin, x_gen1, None]
        ey += [0.0, y, None]
    fig.add_trace(go.Scatter(
        x=ex, y=ey, mode="lines", line=dict(color="#c9c9c9", width=1.6),
        name="architecture inherited from NLP", hoverinfo="skip",
    ))

    # each Gen-1 model → the reckoning (fails the linear-baseline test).
    ex, ey = [], []
    for y in gen1_y:
        ex += [x_gen1, x_reck, None]
        ey += [y, 0.0, None]
    fig.add_trace(go.Scatter(
        x=ex, y=ey, mode="lines", line=dict(color="#e9a8a8", width=1.6),
        name="fails the linear-baseline test (the reckoning)", hoverinfo="skip",
    ))

    # reckoning → each Gen-2 response, coloured by which cause it fixes.
    for cause, color in CAUSE_COLOR.items():
        ex, ey = [], []
        for (_, c, _), y in zip(GEN2, gen2_y):
            if c != cause:
                continue
            ex += [x_reck, x_gen2, None]
            ey += [0.0, y, None]
        if ex:
            fig.add_trace(go.Scatter(
                x=ex, y=ey, mode="lines", line=dict(color=color, width=2.2),
                name=CAUSE_LABEL[cause], hoverinfo="skip",
            ))

    # ── nodes ────────────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=[origin_pos[0]], y=[origin_pos[1]],
        mode="markers+text", text=["NLP transformer"], textposition="bottom center",
        textfont=dict(size=11, color="#333"),
        marker=dict(size=26, color="#7f7f7f", line=dict(color="#333", width=1)),
        name="", showlegend=False,
        hovertext=["BERT- / GPT-shaped architecture — designed for sequential, "
                   "dense, ordered language tokens, not sparse unordered transcriptomics."],
        hoverinfo="text",
    ))
    fig.add_trace(go.Scatter(
        x=[x_gen1] * len(GEN1), y=gen1_y,
        mode="markers+text", text=[g[0] for g in GEN1], textposition="top center",
        textfont=dict(size=11, color="#333"),
        marker=dict(size=20, color="#1f77b4", line=dict(color="#333", width=1)),
        name="", showlegend=False,
        hovertext=[g[1] for g in GEN1], hoverinfo="text",
    ))
    fig.add_trace(go.Scatter(
        x=[reck_pos[0]], y=[reck_pos[1]],
        mode="markers",
        marker=dict(size=30, color="#d62728", symbol="diamond",
                    line=dict(color="#333", width=1)),
        name="", showlegend=False,
        hovertext=["A linear baseline beats every published sc-FM on perturbation "
                   "prediction. Four overlapping causes: (1) the training objective "
                   "optimizes correlation, (2) the architecture inherits NLP, "
                   "(3) the evaluations were systematically biased, "
                   "(4) sc-FMs encode cell-type/pathway features but not regulatory logic."],
        hoverinfo="text",
    ))
    gen2_colors = [CAUSE_COLOR[c] for (_, c, _) in GEN2]
    fig.add_trace(go.Scatter(
        x=[x_gen2] * len(GEN2), y=gen2_y,
        mode="markers+text", text=[g[0] for g in GEN2], textposition="middle right",
        textfont=dict(size=11, color="#333"),
        marker=dict(size=20, color=gen2_colors, line=dict(color="#333", width=1)),
        name="", showlegend=False,
        hovertext=[g[2] for g in GEN2], hoverinfo="text",
    ))

    # The reckoning node label — its own annotation so it clears the
    # edges fanning out to the right.
    fig.add_annotation(x=x_reck, y=-0.62, text="The 2025 reckoning",
                       showarrow=False, font=dict(size=11, color="#333"),
                       yanchor="top")

    # ── column headers ───────────────────────────────────────────────────
    for x, label in [
        (x_origin, "2017<br>NLP origin"),
        (x_gen1, "2023–24<br>Gen-1 sc-FMs"),
        (x_reck, "2025<br>the reckoning"),
        (x_gen2, "2026<br>the response"),
    ]:
        fig.add_annotation(x=x, y=2.95, text=f"<b>{label}</b>", showarrow=False,
                           font=dict(size=11, color="#666"), yanchor="bottom",
                           align="center")

    fig.update_layout(
        title=dict(
            text=(
                "Foundation-model lineage — the field answering itself<br>"
                "<sub>Gen-1 sc-FMs inherited the NLP transformer, lost to a linear "
                "baseline, and the 2026 response fixes the causes. Hover any node.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(visible=False, range=[-0.6, 4.5]),
        yaxis=dict(visible=False, range=[-2.7, 3.3]),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#bbb", borderwidth=1,
                    x=0.5, xanchor="center", y=-0.04, yanchor="top",
                    orientation="h"),
        margin=dict(l=30, r=30, t=80, b=90),
        height=560,
    )
    write_fig(fig, "fm-lineage-tree.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 4 — agentic AI × foundation models: the four patterns
# Source: docs/talks/fm-to-virtual-cells/agentic-meets-foundation.md
# ─────────────────────────────────────────────────────────────────────────────

PATTERNS = [
    dict(name="Pattern 1<br>FM as tool", x=0.27, y=0.27,
         exemplar="PathChat-DX · MedAgentGym · Owkin Pathology Explorer",
         structure="LLM agent calls a frozen biology FM the way it calls a calculator.",
         why="Makes biology FMs usable by clinicians who can't write PyTorch."),
    dict(name="Pattern 4<br>FM as analysis<br>substrate", x=0.36, y=0.45,
         exemplar="CellVoyager (Nat Methods 2026)",
         structure="Autonomous comp-bio agent runs a full analysis end-to-end, calling FMs as needed.",
         why="The pattern closest to a working scientist's daily loop — produces analyses, not answers."),
    dict(name="Pattern 3<br>FM as verifier", x=0.63, y=0.58,
         exemplar="rBio v1 (CZ Biohub 2025)",
         structure="LLM post-trained with RL where a biology FM is the plausibility verifier.",
         why="Inverts tool-use — the FM shapes the agent during training. First virtual-cell reasoning model."),
    dict(name="Pattern 2<br>FM builder", x=0.74, y=0.74,
         exemplar="VCHarness (BioMap + MBZUAI 2026)",
         structure="LLM + coding agent autonomously designs and trains a virtual-cell architecture.",
         why="Changes who can build a virtual cell — months to days."),
]


def build_agentic_patterns() -> None:
    fig = go.Figure()

    # Quadrant background tints.
    fig.add_shape(type="rect", x0=0, y0=0, x1=0.5, y1=0.5,
                  fillcolor="#eef4fb", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=1, y1=1,
                  fillcolor="#fdf2e6", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=0, y0=0.5, x1=0.5, y1=1,
                  fillcolor="#f5f5f5", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=0.5, y0=0, x1=1, y1=0.5,
                  fillcolor="#f5f5f5", line_width=0, layer="below")
    # Mid grid lines + the diagonal the four systems sit on.
    fig.add_shape(type="line", x0=0.5, y0=0, x1=0.5, y1=1,
                  line=dict(color="#ccc", width=1))
    fig.add_shape(type="line", x0=0, y0=0.5, x1=1, y1=0.5,
                  line=dict(color="#ccc", width=1))
    fig.add_shape(type="line", x0=0.08, y0=0.05, x1=0.95, y1=0.95,
                  line=dict(color="#bbb", width=1.5, dash="dot"))

    # Quadrant labels — the two diagonal quadrants get their label tucked
    # into the off-diagonal corner so it clears the bubbles.
    fig.add_annotation(x=0.25, y=0.93, showarrow=False, align="center",
                       font=dict(size=11, color="#999"),
                       text="(rare)<br>consume an FM → produce a model")
    fig.add_annotation(x=0.75, y=0.08, showarrow=False, align="center",
                       font=dict(size=11, color="#999"),
                       text="(rare)<br>build an FM → produce one answer")
    fig.add_annotation(x=0.03, y=0.06, showarrow=False, align="left",
                       xanchor="left", font=dict(size=11, color="#2c6fb0"),
                       text="<b>CONSUME a finished FM<br>→ produce a result</b>")
    fig.add_annotation(x=0.97, y=0.94, showarrow=False, align="right",
                       xanchor="right", font=dict(size=11, color="#c87a1e"),
                       text="<b>ENGAGE with FM construction<br>→ produce a model</b>")

    fig.add_trace(go.Scatter(
        x=[p["x"] for p in PATTERNS],
        y=[p["y"] for p in PATTERNS],
        mode="markers+text",
        text=[p["name"] for p in PATTERNS],
        textposition="middle center",
        textfont=dict(size=9, color="white"),
        marker=dict(size=92, color=["#1f77b4", "#1f77b4", "#ff7f0e", "#ff7f0e"],
                    opacity=0.92, line=dict(color="#333", width=1.5)),
        customdata=[[p["exemplar"], p["structure"], p["why"]] for p in PATTERNS],
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Exemplar: %{customdata[0]}<br>"
            "%{customdata[1]}<br>"
            "<i>%{customdata[2]}</i>"
            "<extra></extra>"
        ),
        showlegend=False,
    ))

    fig.add_annotation(x=0.5, y=1.07, showarrow=False, xref="x", yref="y",
                       font=dict(size=10, color="#888"),
                       text="The four public 2024–2026 systems cluster on the diagonal")

    fig.update_layout(
        title=dict(
            text=(
                "Agentic AI × foundation models — the four patterns<br>"
                "<sub>Not an orthogonal 2×2 — the public systems run along one "
                "diagonal, from FM-consumers to FM-producers.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(
            title="FM is the engine the agent calls   →   FM is what the agent builds or learns from",
            range=[0, 1], showticklabels=False, zeroline=False, gridcolor="#fff",
        ),
        yaxis=dict(
            title="Output is an answer / analysis   →   Output is a model",
            range=[0, 1.12], showticklabels=False, zeroline=False, gridcolor="#fff",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=70, r=40, t=80, b=70),
        height=560,
    )
    write_fig(fig, "agentic-fm-patterns.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5 — the compute landscape, and the linear baseline that beats it
# Source: docs/talks/fm-to-virtual-cells-supplementary.md §D
# ─────────────────────────────────────────────────────────────────────────────

MODELS = [
    dict(name="Linear baseline", params=10, cost=2, domain="baseline",
         disclosure="n/a",
         note="One-line linear regression on average post-perturbation expression. "
              "Beats every published sc-FM on perturbation prediction.",
         source="Ahlmann-Eltze & Huber 2025"),
    dict(name="Generative VC POC", params=1_000_000, cost=250, domain="sc-FM",
         disclosure="DISCLOSED",
         note="Small MLP/transformer on a Perturb-seq simulator; <100 GPU-hours.",
         source="Lewis & Zueco, ICLR 2026"),
    dict(name="scGPT", params=51_000_000, cost=25000, cost_lo=2600, cost_hi=250000,
         domain="sc-FM", disclosure="UNKNOWN",
         note="~51M params; 33M cells. Cui 2024 discloses no compute — a 50× cost band.",
         source="Cui 2024 Nat Methods"),
    dict(name="Geneformer V2-104M", params=104_000_000, cost=17000, domain="sc-FM",
         disclosure="DISCLOSED",
         note="64× A100 80GB · 6,656 GPU-hours. Cheapest fully-disclosed sc-FM training.",
         source="NVIDIA BioNeMo recipe"),
    dict(name="Geneformer V2-316M", params=316_000_000, cost=30000, domain="sc-FM",
         disclosure="DISCLOSED",
         note="128× A100 · 11,576 GPU-hours. Matched by the 104M domain-curated model.",
         source="NVIDIA BioNeMo recipe"),
    dict(name="UCE", params=650_000_000, cost=22000, cost_lo=3000, cost_hi=175000,
         domain="sc-FM", disclosure="UNKNOWN",
         note="650M params; ~36M cells. Largest sc-FM, least transparent on cost.",
         source="Rosen 2024 Nat Methods"),
    dict(name="STATE (SE-600M)", params=600_000_000, cost=125000, domain="sc-FM",
         disclosure="UNKNOWN",
         note="600M-param embedding module; 167M cells. Order-of-magnitude cost estimate.",
         source="Adduri 2025 bioRxiv"),
    dict(name="UNI2-h", params=681_000_000, cost=75000, domain="pathology",
         disclosure="UNKNOWN",
         note="681M-param ViT-H/14; 200M+ tiles across 350K+ slides. Cost estimated.",
         source="Chen 2024 HF card"),
    dict(name="AlphaGenome", params=450_000_000, cost=200000, domain="genomic",
         disclosure="partial",
         note="~450M params; 8× TPU v3 per replica × 4-fold ensemble + distillation. Cost estimated.",
         source="Avsec 2025 Nature"),
    dict(name="Evo2 (40B)", params=40_000_000_000, cost=5_000_000, domain="genomic",
         disclosure="DISCLOSED",
         note="40B params; 2,048× H100 · ~2,000,000 GPU-hours.",
         source="Brixi 2026 Nature"),
    dict(name="ESM-3 (98B)", params=98_000_000_000, cost=4_500_000,
         cost_lo=2_500_000, cost_hi=8_000_000, domain="protein",
         disclosure="DISCLOSED",
         note="98B params; 1.07×10²⁴ FLOPs disclosed.",
         source="Hayes 2025 Science"),
]

DOMAIN_COLOR = {
    "sc-FM": "#1f77b4",
    "pathology": "#ff7f0e",
    "genomic": "#2ca02c",
    "protein": "#9467bd",
    "baseline": "#d62728",
}

# Manual label placement — the sc-FM cluster is genuinely tight, so each
# label gets a hand-picked side to keep them legible.
LABEL_POS = {
    "Linear baseline": "middle right",
    "Generative VC POC": "top center",
    "scGPT": "top left",
    "Geneformer V2-104M": "bottom center",
    "Geneformer V2-316M": "middle right",
    "UCE": "bottom right",
    "STATE (SE-600M)": "top left",
    "UNI2-h": "bottom right",
    "AlphaGenome": "top center",
    "Evo2 (40B)": "bottom left",
    "ESM-3 (98B)": "top left",
}


def build_compute_landscape() -> None:
    fig = go.Figure()

    # Reference bands.
    fig.add_hline(y=17000, line=dict(color="#888", width=1, dash="dot"))
    fig.add_hline(y=5_000_000, line=dict(color="#888", width=1, dash="dot"))
    fig.add_annotation(x=math.log10(11), y=math.log10(17000),
                       text="$17k — cheapest fully-disclosed sc-FM",
                       showarrow=False, xanchor="left", yanchor="bottom",
                       font=dict(size=10, color="#666"))
    fig.add_annotation(x=math.log10(11), y=math.log10(5_000_000),
                       text="~$5M — the frontier ceiling (Evo2 / ESM-3)",
                       showarrow=False, xanchor="left", yanchor="bottom",
                       font=dict(size=10, color="#666"))

    for domain, color in DOMAIN_COLOR.items():
        sub = [m for m in MODELS if m["domain"] == domain]
        if not sub:
            continue
        is_baseline = domain == "baseline"
        symbols = []
        for m in sub:
            if is_baseline:
                symbols.append("star")
            elif m["disclosure"] == "DISCLOSED":
                symbols.append("circle")
            else:
                symbols.append("circle-open")
        err = dict(
            type="data", symmetric=False,
            array=[m.get("cost_hi", m["cost"]) - m["cost"] for m in sub],
            arrayminus=[m["cost"] - m.get("cost_lo", m["cost"]) for m in sub],
            color=color, thickness=1, width=4,
        )
        fig.add_trace(go.Scatter(
            x=[m["params"] for m in sub],
            y=[m["cost"] for m in sub],
            mode="markers+text",
            name=("linear baseline" if is_baseline else domain),
            text=[m["name"] for m in sub],
            textposition=[LABEL_POS.get(m["name"], "top center") for m in sub],
            textfont=dict(size=9, color="#333"),
            marker=dict(size=[26 if is_baseline else 14 for _ in sub],
                        color=color, symbol=symbols,
                        line=dict(color=color, width=2)),
            error_y=err,
            customdata=[[m["disclosure"], m["note"], m["source"]] for m in sub],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Parameters: %{x:,}<br>"
                "Est. training cost: $%{y:,.0f}<br>"
                "Disclosure: %{customdata[0]}<br>"
                "%{customdata[1]}<br>"
                "<i>Source: %{customdata[2]}</i>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        title=dict(
            text=(
                "The compute landscape — and the linear baseline that beats it<br>"
                "<sub>Filled = training cost disclosed; open = undisclosed/estimated "
                "(bars show the cost band). The red star is the parameter-free "
                "linear baseline. Hover for the source.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(title="Parameters (log scale)", type="log",
                   gridcolor="#e6e6e6", range=[math.log10(7), math.log10(1.2e12)]),
        yaxis=dict(title="Estimated training cost, USD (log scale)", type="log",
                   gridcolor="#e6e6e6", range=[math.log10(1), math.log10(2e7)]),
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
        legend=dict(title="FM domain", bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#bbb", borderwidth=1,
                    x=0.98, xanchor="right", y=0.02, yanchor="bottom"),
        margin=dict(l=80, r=40, t=80, b=60),
        height=560,
    )
    write_fig(fig, "fm-compute-landscape.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 6 — why linear baselines win: four overlapping causes
# Source: docs/talks/fm-to-virtual-cells/why-linear-baselines-win.md
# ─────────────────────────────────────────────────────────────────────────────

# weight = independent lines of evidence cited in the explainer (May 2026).
CAUSES = [
    dict(short="Cause 1 — wrong training objective",
         weight=2, kind="structural",
         detail="Next-gene-prediction / masked-gene-modelling optimize correlation "
                "between adjacent gene tokens; perturbation prediction wants a causal "
                "counterfactual. Different problems — correlational pretraining doesn't "
                "transfer.",
         track="Track 2 — counterfactual / IRM / contrastive-perturbation pretraining"),
    dict(short="Cause 2 — NLP architecture, not biology",
         weight=3, kind="structural",
         detail="Every major sc-FM is a BERT/GPT-shaped transformer built for ordered "
                "dense language tokens. Transcriptomics is sparse, unordered, "
                "biologically structured. xVERSE shows the architectural choice is "
                "empirically load-bearing (+17.9% representation).",
         track="Track 4 — graph-attention, pathway priors, lineage-aware encoders"),
    dict(short="Cause 3 — biased evaluation methodology",
         weight=4, kind="corrected",
         detail="Splitting on cells not perturbations, averaging metrics that hide "
                "big-effect failures, selective benchmark curation. Not fraud — "
                "accreted reasonable choices that built a false leaderboard. The "
                "reckoning itself corrected this.",
         track="Track 6 — causal-recovery benchmarks (MR-validated + LINCS + ENCODE)"),
    dict(short="Cause 4 — what sc-FMs actually encode",
         weight=3, kind="structural",
         detail="Sparse autoencoders on sc-FM activations recover cell-type and "
                "pathway features cleanly, but fail to recover regulatory / causal "
                "features. A mechanistic explanation of Cause 1.",
         track="Track 1 — mechanistic interpretability (cancer-curated SAE atlases)"),
    dict(short="Framing — causal transportability (Pearl)",
         weight=1, kind="structural",
         detail="Virtual Cells Need Context (2026) frames the failure as a causal "
                "transportability problem: a model trained on P(X|do(Y),Z=z₁) does not "
                "predict in Z=z₂. Not capacity-bounded — structural.",
         track="Track 9 — causal transportability benchmark suite (still unwritten)"),
    dict(short="Contrarian — scale may dissolve Causes 1–4",
         weight=1, kind="contested",
         detail="FMs Improve Perturbation Response Prediction (bioRxiv 2026.02.18) "
                "argues that with sufficient data FMs DO improve genetic + chemical "
                "perturbation prediction and approach fundamental limits. The "
                "reckoning is contested, not closed.",
         track="If right: the work is scaling + data curation (Lane 3, Lane 5)"),
]

KIND_COLOR = {
    "structural": "#d62728",
    "corrected": "#7f7f7f",
    "contested": "#2ca02c",
}
KIND_LABEL = {
    "structural": "structural — more scale alone won't fix it",
    "corrected": "already corrected by the reckoning",
    "contested": "contested — the contrarian says scale may fix it",
}


def build_four_causes() -> None:
    # Reverse so Cause 1 sits at the top of the horizontal bar chart.
    rows = list(reversed(CAUSES))
    fig = go.Figure()

    for kind, color in KIND_COLOR.items():
        sub = [r for r in rows if r["kind"] == kind]
        if not sub:
            continue
        fig.add_trace(go.Bar(
            x=[r["weight"] for r in sub],
            y=[r["short"] for r in sub],
            orientation="h",
            name=KIND_LABEL[kind],
            marker=dict(color=color, line=dict(color="#333", width=1)),
            customdata=[[r["detail"], r["track"]] for r in sub],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{customdata[0]}<br>"
                "<i>Addressed by: %{customdata[1]}</i>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        title=dict(
            text=(
                "Why linear baselines win — four overlapping causes, not one<br>"
                "<sub>Bar = independent lines of evidence in the literature; "
                "colour = is the cause fixable with scale?</sub>"
            ),
            font=dict(size=15),
        ),
        barmode="stack",
        xaxis=dict(title="Independent lines of supporting evidence",
                   gridcolor="#e6e6e6", dtick=1, range=[0, 4.6]),
        yaxis=dict(automargin=True, categoryorder="array",
                   categoryarray=[r["short"] for r in rows]),
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
        legend=dict(title="Is the cause fixable with scale?",
                    bgcolor="rgba(255,255,255,0.95)", bordercolor="#bbb",
                    borderwidth=1, orientation="h",
                    x=0.5, xanchor="center", y=-0.22, yanchor="top"),
        margin=dict(l=40, r=40, t=85, b=95),
        height=470,
    )
    write_fig(fig, "fm-four-causes.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 7 — cause × small-lab-track matrix
# Source: why-linear-baselines-win.md + supplementary §C / §G.1
# ─────────────────────────────────────────────────────────────────────────────

TRACKS = [
    ("T1 — Mechanistic interpretability",
     "What do scGPT / Geneformer / UNI actually learn?"),
    ("T2 — Causality-targeting pretraining",
     "Next-gene-prediction optimizes correlation — that's why FMs lose to linear baselines"),
    ("T3 — Compositional benchmarks + theory",
     "Does A+B generalize when the model saw only A and B separately?"),
    ("T4 — Biology-specific architectures",
     "BERT clones ignore pathway / network / lineage priors"),
    ("T5 — UQ / OOD detection",
     "Every FDA path needs calibrated uncertainty; FMs don't have it"),
    ("T6 — Causal evaluation frameworks",
     "What's the correct test for causality, post-Ahlmann-Eltze?"),
    ("T7 — Cross-species / phylogenetic priors",
     "Does cross-species pretraining help or hurt for cancer biology?"),
    ("T8 — Synergistic-info evaluation",
     "Which fusion strategies buy cross-modal information vs redundancy?"),
    ("T9 — Causal transportability benchmarks",
     "What's the right test for cross-context generalization, post-VCsNC?"),
]

CAUSE_COLS = [
    "Cause 1<br>objective", "Cause 2<br>architecture", "Cause 3<br>eval bias",
    "Cause 4<br>what FMs encode", "Theoretical<br>framing",
]

# Row per track, column order matches CAUSE_COLS. 2 = directly addresses,
# 1 = partially addresses, 0 = not really.
TRACK_CAUSE = [
    [1, 0, 0, 2, 0],  # T1
    [2, 0, 1, 1, 1],  # T2
    [0, 0, 2, 0, 1],  # T3
    [1, 2, 0, 0, 0],  # T4
    [0, 0, 1, 1, 0],  # T5
    [1, 0, 2, 0, 1],  # T6
    [0, 1, 0, 0, 1],  # T7
    [0, 0, 1, 0, 1],  # T8
    [1, 0, 1, 0, 2],  # T9
]

_CELL_TEXT = {0: "", 1: "partial", 2: "direct"}


def build_cause_track_matrix() -> None:
    track_labels = [t[0] for t in TRACKS]
    track_probs = [t[1] for t in TRACKS]

    text = [[_CELL_TEXT[v] for v in row] for row in TRACK_CAUSE]
    customdata = [
        [[track_probs[i], CAUSE_COLS[j].replace("<br>", " ")] for j in range(5)]
        for i in range(len(TRACKS))
    ]

    fig = go.Figure(go.Heatmap(
        z=TRACK_CAUSE,
        x=CAUSE_COLS,
        y=track_labels,
        text=text,
        texttemplate="%{text}",
        textfont=dict(size=10, color="#222"),
        customdata=customdata,
        colorscale=[[0.0, "#f4f4f4"], [0.5, "#9ecae1"], [1.0, "#2c6fb0"]],
        zmin=0, zmax=2,
        xgap=3, ygap=3,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Open problem: %{customdata[0]}<br>"
            "Relevance to %{customdata[1]}: <b>%{z}</b> (0 none · 1 partial · 2 direct)"
            "<extra></extra>"
        ),
        colorbar=dict(title="addresses", tickvals=[0, 1, 2],
                      ticktext=["none", "partial", "direct"], len=0.6),
    ))

    fig.update_layout(
        title=dict(
            text=(
                "From diagnosis to project — which small-lab track attacks which cause<br>"
                "<sub>Rows = the 9 innovation tracks; columns = the four causes + the "
                "framing. Hover a cell for the open problem.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(side="top", tickfont=dict(size=10), tickangle=0),
        yaxis=dict(autorange="reversed", tickfont=dict(size=10), automargin=True),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=150, b=30),
        height=560,
    )
    write_fig(fig, "fm-cause-track-matrix.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 8 — the 2023–2026 arc as three interleaved swimlanes
# Source: docs/talks/fm-to-virtual-cells.md §1.3 + evaluation-papers-catalog.md
# ─────────────────────────────────────────────────────────────────────────────

# (date YYYY-MM, short label, detail). Release dates are month-level
# first-public-appearance (preprint or journal).
ARC_RELEASES = [
    ("2023-05", "scGPT", "Next-gene-prediction transformer — defined the sc-FM category."),
    ("2023-06", "Geneformer", "Masked-gene-modelling transformer; the other canonical Gen-1 sc-FM."),
    ("2024-02", "UCE", "Universal Cell Embedding — cross-species via ESM2-bridged tokenization."),
    ("2024-05", "CellPLM", "Cell-as-token pretraining; included in most 2026 evaluation sweeps."),
    ("2024-06", "scFoundation", "Read-depth-aware attention — closest Gen-1 model to architecture–biology co-design."),
    ("2025-06", "TranscriptFormer", "Generative cross-species architecture; 112M cells × 12 species (CZ Biohub)."),
    ("2025-09", "STATE", "600M-param embedding + transition model on 167M cells (Arc Institute)."),
    ("2026-03", "TxPert", "Multiple-knowledge-graph perturbation prediction — the reckoning answering itself."),
    ("2026-04", "xVERSE", "Transcriptomics-native (non-LM) architecture; +17.9% representation over LM-derived sc-FMs."),
]
ARC_RECKONING = [
    ("2024-09", "Csendes", "scPerturBench — the original scGPT split was leaky."),
    ("2025-04", "Kedzierska", "scFMs lose to PCA + kNN zero-shot (Genome Biology)."),
    ("2025-07", "Wenkel", "latent-additive + scGPT-embeddings is the new baseline floor (Nat Methods)."),
    ("2025-07", "PertEval-scFM", "Most scFM embeddings don't beat baselines on strong perturbations (ICML)."),
    ("2025-08", "Ahlmann-Eltze", "THE canonical blow — no sc-FM beats a one-line linear baseline (<$2k compute)."),
    ("2025-10", "Wu (Genome Biol)", "No single scFM consistently outperforms others across tasks."),
    ("2026-01", "Wu (Nat Methods)", "Axis-by-axis failure decomposition — 27 methods × 29 datasets."),
    ("2026-01", "Liu (scEval)", "Challenges the necessity of developing FMs for single-cell analysis."),
    ("2026-02", "Parameter-free", "Parameter-free representations win on downstream benchmarks."),
    ("2026-03", "Cellular-dynamics", "zero-shot scFMs fail to recover RNA-velocity / cellular dynamics."),
    ("2026-04", "CellBench-LS", "Low-supervision: FMs lead cell-type, classical leads gene-expression."),
    ("2026-04", "Han et al.", "Industry-grade robustness gaps in real-world data integration."),
]
ARC_RESPONSE = [
    ("2025-11", "rBio", "First virtual-cell reasoning model — RL with an FM as plausibility verifier (CZ Biohub)."),
    ("2026-01", "Theis — compositional FMs", "Cell Systems Perspective: stop training monolithic sc-FMs, compose modality-specific FMs."),
    ("2026-02", "Contrarian voice", "FMs Improve Perturbation — with enough data, FMs DO improve. The reckoning is contested."),
    ("2026-02", "Virtual Cells Need Context", "Names the theoretical framing — causal transportability (Pearl)."),
    ("2026-02", "CellVoyager", "Autonomous comp-bio agent runs full analyses end-to-end (Nat Methods)."),
    ("2026-04", "VCHarness", "LLM + coding agent autonomously designs and trains a virtual-cell architecture."),
]

ARC_LANES = [
    ("sc-FM & architecture releases", 2.0, "#1f77b4", ARC_RELEASES),
    ("the reckoning corpus", 1.0, "#d62728", ARC_RECKONING),
    ("framing & agentic response", 0.0, "#2ca02c", ARC_RESPONSE),
]


def build_arc_timeline() -> None:
    fig = go.Figure()

    for lane_name, y, color, events in ARC_LANES:
        ev = sorted(events, key=lambda e: e[0])
        xs = [_ts(d) for d, _, _ in ev]
        # lane guide line
        fig.add_shape(type="line", x0=xs[0], x1=xs[-1],
                      y0=y, y1=y, line=dict(color=color, width=1.4),
                      layer="below")
        # thin labels: only show one if it's ≥5 months from the last shown
        # label, so the dense 2026 cluster stays legible. Hover covers the rest.
        labels, textpos, last_shown = [], [], None
        flip = 0
        for d, lbl, _ in ev:
            ts = _ts(d)
            if last_shown is None or (ts - last_shown).days >= 150:
                labels.append(lbl)
                textpos.append("top center" if flip % 2 == 0 else "bottom center")
                flip += 1
                last_shown = ts
            else:
                labels.append("")
                textpos.append("top center")
        fig.add_trace(go.Scatter(
            x=xs, y=[y] * len(ev),
            mode="markers+text",
            name=lane_name,
            text=labels,
            textposition=textpos,
            textfont=dict(size=9, color="#444"),
            marker=dict(size=12, color=color, line=dict(color="#fff", width=1.2)),
            customdata=[[lbl, d, detail] for d, lbl, detail in ev],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>%{customdata[1]}<br>"
                "<i>%{customdata[2]}</i><extra></extra>"
            ),
        ))

    # Lane labels on the left margin.
    for lane_name, y, color, _ in ARC_LANES:
        fig.add_annotation(x=_ts("2023-02"), y=y, text=f"<b>{lane_name}</b>",
                           showarrow=False, xanchor="right",
                           font=dict(size=10, color=color))

    fig.add_annotation(
        x=_ts("2025-08"), y=1.0, ax=0, ay=-46, arrowhead=2, arrowcolor="#888",
        text="Aug 2025 — the canonical blow", font=dict(size=10, color="#555"),
    )

    fig.update_layout(
        title=dict(
            text=(
                "The 2023–2026 arc — reckoning and response are interleaved, not sequential<br>"
                "<sub>Three swimlanes on one time axis: the architecture critiques land "
                "<i>while</i> the next-generation models ship.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(title="", gridcolor="#e6e6e6", range=["2022-10-01", "2026-08-01"]),
        yaxis=dict(visible=False, range=[-0.9, 2.9]),
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
        showlegend=False,
        margin=dict(l=160, r=40, t=80, b=40),
        height=420,
    )
    write_fig(fig, "fm-arc-timeline.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 9 — the evaluation corpus by venue tier
# Source: docs/talks/fm-to-virtual-cells/evaluation-papers-catalog.md
# ─────────────────────────────────────────────────────────────────────────────

# venue tier: 3 = peer-reviewed journal, 2 = conference, 1 = preprint.
VENUE_TIER = {
    "Csendes scPerturBench": 1,
    "Kedzierska et al.": 3,
    "Wenkel et al.": 3,
    "PertEval-scFM": 2,
    "Ahlmann-Eltze & Huber": 3,
    "Wu et al. (Genome Biology)": 3,
    "Wu et al. (Nat Methods)": 3,
    "Liu et al. (scEval)": 3,
    "Parameter-free baseline": 1,
    "Cellular-dynamics zero-shot": 1,
    "CellBench-LS": 1,
    "Han et al. (real-world)": 1,
}
TIER_LABEL = {3: "Peer-reviewed<br>journal", 2: "Conference", 1: "Preprint"}


def build_eval_catalog_timeline() -> None:
    rows = sorted(RECKONING, key=lambda r: r["date"])
    fig = go.Figure()

    # gentle vertical jitter so same-month / same-tier papers don't fully overlap.
    seen: dict[tuple[str, int], int] = {}

    for axis, color in AXIS_COLOR.items():
        sub = [r for r in rows if r["axis"] == axis]
        if not sub:
            continue
        xs, ys, cd = [], [], []
        for r in sub:
            tier = VENUE_TIER[r["name"]]
            key = (r["date"], tier)
            k = seen.get(key, 0)
            seen[key] = k + 1
            xs.append(_ts(r["date"]))
            ys.append(tier + (k * 0.16))
            cd.append([r["name"], r["venue"], r["date"], r["headline"], r["models"]])
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="markers",
            name=AXIS_LABEL[axis],
            marker=dict(size=15, color=color, line=dict(color="#fff", width=1.5)),
            customdata=cd,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]} · %{customdata[2]}<br>"
                "Models: %{customdata[4]}<br>"
                "<i>%{customdata[3]}</i><extra></extra>"
            ),
        ))

    # contrarian voice — preprint tier, distinct green ✕.
    fig.add_trace(go.Scatter(
        x=[_ts(CONTRARIAN["date"])], y=[1 + 0.16],
        mode="markers", name="The contrarian voice",
        marker=dict(size=16, color="#2ca02c", symbol="x",
                    line=dict(color="#1a661a", width=1)),
        customdata=[[CONTRARIAN["name"], CONTRARIAN["venue"], CONTRARIAN["date"],
                     CONTRARIAN["headline"], CONTRARIAN["models"]]],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "%{customdata[1]} · %{customdata[2]}<br>"
            "Models: %{customdata[4]}<br>"
            "<i>%{customdata[3]}</i><extra></extra>"
        ),
    ))

    fig.update_layout(
        title=dict(
            text=(
                "The reckoning corpus by venue tier — not one lab's grievance<br>"
                "<sub>13 papers, 2024–2026 — six cleared peer review "
                "(Nature Methods ×3, Genome Biology, Advanced Science).</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(title="Publication date", gridcolor="#e6e6e6",
                   range=["2024-06-01", "2026-06-01"]),
        yaxis=dict(tickvals=[1, 2, 3], ticktext=[TIER_LABEL[t] for t in (1, 2, 3)],
                   gridcolor="#e6e6e6", range=[0.5, 3.6]),
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
        legend=dict(title="Evaluation axis", bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#bbb", borderwidth=1, orientation="h",
                    x=0.5, xanchor="center", y=-0.2, yanchor="top"),
        margin=dict(l=110, r=40, t=85, b=95),
        height=470,
    )
    write_fig(fig, "fm-eval-catalog-timeline.html")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 10 — institutional landscape: who builds vs who audits
# Source: docs/talks/fm-to-virtual-cells-supplementary.md §F
# The build / critique scores are a qualitative reading of §F — a speaker's
# judgement call, not a measured metric.
# ─────────────────────────────────────────────────────────────────────────────

INSTITUTES = [
    dict(name="Arc Institute", group="builder", build=10, crit=1.5,
         pi="Hsu + Goodarzi", ships="Evo2, STATE, Tahoe-100M",
         why="Largest non-DeepMind compute; sets the perturbation-atlas substrate."),
    dict(name="Mahmood Lab", group="builder", build=9, crit=1,
         pi="Faisal Mahmood", ships="UNI/UNI2-h, CONCH, PathChat-DX, TITAN, CHIEF",
         why="Full pathology vertical stack; first FDA Breakthrough for generative-AI pathology."),
    dict(name="Theodoris Lab", group="builder", build=5.3, crit=2.4,
         pi="Christina Theodoris", ships="Geneformer V1/V2/_CLcancer",
         why="Only academic sc-FM lab with full compute disclosure; domain-curation-beats-scale finding."),
    dict(name="Bo Wang Lab", group="builder", build=6.8, crit=3.4,
         pi="Bo Wang", ships="scGPT, scGPT-spatial, MedSAM",
         why="Defined the sc-FM category; explicit 2025 agentic-AI pivot."),
    dict(name="Leskovec + Quake", group="builder", build=4.5, crit=1.4,
         pi="Leskovec + Quake", ships="UCE",
         why="Cross-species cell embedding (8 species via ESM2-bridge)."),
    dict(name="Google DeepMind", group="builder", build=9.5, crit=2.8,
         pi="Avsec et al.", ships="AlphaGenome, AlphaFold 2/3, Med-Gemini",
         why="TPU-scale; closed weights + hosted API; Isomorphic is the commercial arm."),
    dict(name="EvolutionaryScale", group="builder", build=7.8, crit=2.6,
         pi="Rives, Sercu, Hayes", ships="ESM-3",
         why="Cleanest published FLOPs disclosure in biology FM."),
    dict(name="Paige + MSK", group="builder", build=7.6, crit=1.1,
         pi="Fuchs + Zimmermann", ships="Virchow / Virchow2 / Virchow2G, FullFocus",
         why="First FDA 510(k)-cleared general-purpose pathology AI."),
    dict(name="Owkin", group="builder", build=5.8, crit=1,
         pi="industry consortium", ships="Phikon, Phikon-v2, H-optimus-0, MOSAIC",
         why="Only major industrial pathology player shipping open weights."),
    dict(name="BioMap + MBZUAI", group="builder", build=6.5, crit=2,
         pi="Le Song, Eric Xing", ships="VCHarness, xTrimo PGLM",
         why="China / Middle-East-side competitor to the CZ Biohub stack."),
    dict(name="Zitnik Lab", group="builder", build=4.6, crit=3.6,
         pi="Marinka Zitnik", ships="TxGNN, TDC-2",
         why="Graph-FM-for-clinic; bridges sc-FMs and agentic clinical AI."),
    dict(name="NVIDIA BioNeMo", group="infrastructure", build=3.6, crit=2.9,
         pi="framework team", ships="BioNeMo framework; Geneformer V2 recipe; Evo2 co-author",
         why="Sets the compute-disclosure norm as a co-marketing artifact."),
    dict(name="CZ Biohub + CZI", group="does both", build=7, crit=5,
         pi="Karaletsos, Quake, Pisco",
         ships="CELLxGENE Census, Tabula Sapiens, TranscriptFormer, rBio",
         why="Now ships BOTH substrate and model — breaks the substrate-only stereotype."),
    dict(name="Theis Lab", group="does both", build=5, crit=7,
         pi="Fabian Theis", ships="scvi-tools, scArches, compositional-FM Perspective",
         why="The methodological reference class for the whole field."),
    dict(name="Ahlmann-Eltze + Huber", group="critique anchor", build=1, crit=9,
         pi="Ahlmann-Eltze + Huber", ships="The 2025 linear-baseline paper",
         why="Retired the sc-FM perturbation leaderboard — the canonical reckoning."),
    dict(name="Kedzierska + Lu", group="critique anchor", build=1, crit=7,
         pi="Kedzierska + Lu", ships="The zero-shot extension of the reckoning",
         why="Extended the linear-baseline result to UCE and the zero-shot setting."),
    dict(name="Aviv Regev @ Genentech", group="agenda-setter", build=2, crit=4,
         pi="Aviv Regev", ships="Rood + Regev 2024 Cell agenda",
         why="Agenda-setter for 'causal foundation models of cells'; largest pharma buyer."),
]

GROUP_COLOR = {
    "builder": "#1f77b4",
    "infrastructure": "#7f7f7f",
    "does both": "#9467bd",
    "critique anchor": "#d62728",
    "agenda-setter": "#ff7f0e",
}

# hand-picked label sides — the dense builder cluster alternates top/bottom
# within each critique-score row so adjacent labels clear each other.
INST_LABEL_POS = {
    "Arc Institute": "middle left",
    "Mahmood Lab": "bottom center",
    "Paige + MSK": "bottom center",
    "BioMap + MBZUAI": "bottom center",
    "Owkin": "bottom center",
    "Leskovec + Quake": "bottom center",
    "Google DeepMind": "bottom center",
    "EvolutionaryScale": "top center",
    "Bo Wang Lab": "top center",
    "Theodoris Lab": "top center",
    "Zitnik Lab": "top center",
    "NVIDIA BioNeMo": "middle left",
    "CZ Biohub + CZI": "top center",
    "Theis Lab": "middle left",
    "Ahlmann-Eltze + Huber": "bottom right",
    "Kedzierska + Lu": "bottom right",
    "Aviv Regev @ Genentech": "middle right",
}


def build_institutional_landscape() -> None:
    fig = go.Figure()

    # the "does both" diagonal — institutes near it both build and audit.
    fig.add_shape(type="line", x0=0, y0=0, x1=10, y1=10,
                  line=dict(color="#bbb", width=1.5, dash="dot"), layer="below")
    fig.add_annotation(x=1.7, y=1.7, text="the rare \"does both\" diagonal",
                       showarrow=False, font=dict(size=10, color="#999"),
                       textangle=-45)

    for group, color in GROUP_COLOR.items():
        sub = [m for m in INSTITUTES if m["group"] == group]
        if not sub:
            continue
        fig.add_trace(go.Scatter(
            x=[m["build"] for m in sub],
            y=[m["crit"] for m in sub],
            mode="markers+text",
            name=group,
            text=[m["name"] for m in sub],
            textposition=[INST_LABEL_POS.get(m["name"], "top center") for m in sub],
            textfont=dict(size=8, color="#333"),
            marker=dict(size=18, color=color, opacity=0.9,
                        line=dict(color="#333", width=1)),
            customdata=[[m["pi"], m["ships"], m["why"]] for m in sub],
            hovertemplate=(
                "<b>%{text}</b> · %{customdata[0]}<br>"
                "Ships: %{customdata[1]}<br>"
                "<i>%{customdata[2]}</i><extra></extra>"
            ),
        ))

    fig.update_layout(
        title=dict(
            text=(
                "The institutional landscape — who builds FMs vs who audits them<br>"
                "<sub>Most build or audit — few do both. Axes are a qualitative "
                "reading of §F, not a measured metric.</sub>"
            ),
            font=dict(size=15),
        ),
        xaxis=dict(title="FM-building activity  →", gridcolor="#e6e6e6",
                   range=[-0.5, 10.5], zeroline=False),
        yaxis=dict(title="Evaluation / critique activity  →", gridcolor="#e6e6e6",
                   range=[-0.5, 10.5], zeroline=False),
        plot_bgcolor="#fafafa",
        paper_bgcolor="white",
        legend=dict(title="Role in the field", bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#bbb", borderwidth=1,
                    x=0.98, xanchor="right", y=0.98, yanchor="top"),
        margin=dict(l=70, r=40, t=90, b=55),
        height=560,
    )
    write_fig(fig, "fm-institutional-landscape.html")


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    print(f"Building 10 talk figures → {ASSETS.relative_to(REPO_ROOT)}/  ({dt.date.today()})")
    build_reckoning_corpus()
    build_lineage_tree()
    build_lanes_map()
    build_compute_landscape()
    build_agentic_patterns()
    build_four_causes()
    build_cause_track_matrix()
    build_arc_timeline()
    build_eval_catalog_timeline()
    build_institutional_landscape()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
