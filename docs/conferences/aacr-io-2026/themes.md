# AACR IO 2026 — Themes

Fifteen themes across [AACR IO 2026](index.md), with counts from a **keyword census of all 245 published abstracts** harvested via Crossref. Themes overlap, so counts sum to more than 245.

| # | Theme | Abstracts | Program anchor |
|---|---|---|---|
| 1 | Checkpoint biology and resistance | **49** | Keynote 3 (Vignali, Chen); MS3 |
| 2 | Cell therapy — CAR-T/CAR-NK in solid tumors | **24** | MS1, MS7 |
| 3 | Suppressive myeloid compartment | **18** | MS2 |
| 4 | Spatial / single-cell / systems immunology | **18** | SS4; Ed. 1 |
| 5 | Cytokine engineering | **18** | MS6 |
| 6 | Neoantigen discovery and cancer vaccines | **17** | Keynote 1 (Jaffee); SS2 |
| 7 | AI / computational design and biomarkers | **15** | SS1; Ed. 4 |
| 8 | TCR engineering | **14** | MS5 |
| 9 | NK cells | **14** | MS4 |
| 10 | Immunometabolism | **10** | Ed. 3 |
| 11 | B cells and tertiary lymphoid structures | **8** | MS10; Ed. 1 |
| 12 | T-cell engagers / bispecifics | **8** | SS3 |
| 13 | In vivo engineering / LNP / mRNA | **6** | MS7 |
| 14 | Microbiome | **2** | Ed. 2 |
| 15 | Neuro-psych-immunology | not countable | **MS8** |

## Checkpoint biology and resistance — 49 abstracts

The largest theme by a wide margin, and the one the keynote slate is built around. Representative abstracts: **LB-B013**, an 8-pathway transcriptomic biomarker that outperforms PD-L1 for anti-PD-1 response in melanoma; **LB-C004** (NIBIT-ML1, epigenetic reprogramming to overcome PD-1 resistance — see [Readouts](readouts.md)); **B029** on PD-1 inhibitor pharmacovigilance; **B041** on GLP-1 receptor agonists and ICI response.

The biomarker papers here are the direct complement to the [SITC Computational IO series](../sitc-computational-io-2026/index.md), which spends ten webinars on exactly this problem from the methods side.

## Cell therapy in solid tumors — 24 abstracts

The engineering core of the meeting, spanning MS1 (Hinrichs), MS5 (TCR engineering, Witte and Klebanoff), MS6 (TILs, Gastman and Hari), and MS7 (in vivo engineering, Eyquem with Kelonia and Capstan). Representative: **LB-A007** (non-viral site-directed hYP218 mesothelin CAR-T), **A008** (CD5 CAR-NK signal tuning), **B010** (EphA2 CAR-T/NK in NSCLC), **LB-C001** (bispecific CART19/20 — see [Readouts](readouts.md)).

**MS7 is the session to watch.** "In vivo T Cell Engineering – Are We There Yet?" is a full symposium on skipping ex vivo manufacturing entirely, staffed almost entirely by company speakers. Paired with the 6 in vivo/LNP/mRNA abstracts and the **DN64-CAR-V** amphotropic RNA vector (**LB-B011**), this is a modality trying to become a platform in public.

Corpus fit: [`sitc-2026/trials/`](../sitc-2026/trials/index.md) is built to hold exactly these readouts in November.

## Spatial, single-cell, and systems immunology — 18 abstracts

**The strongest direct link to this corpus's core subject matter.**

- **SS4 — Systems Immunology**, chaired by **Garry P. Nolan** (Stanford), with **Linghua Wang** (MD Anderson) on *"A multiscale view of tumor ecosystems: From single-cell states to functional immune niches and communities."*
- **Ed. Session 1** on studying the TME: **Catherine Sautès-Fridman** on spatial determinants of tertiary lymphoid structure formation, **Aaron M. Newman** (Stanford) on noninvasive TME profiling for response assessment.
- **IA01** — Renato Ostuni, *"Spatial and molecular control of tumor immune microenvironment."*
- **Saturday short talk** — Daniel G. Chen (UCLA) on inflammatory spatial niches in desmoplastic melanoma, comparing biopsies from **SWOG S1512 and S1616**. A spatial-omics readout nested inside two cooperative-group trials is an unusually well-controlled use of the technology.

Corpus fit: [`aacr-2026/topics/single-cell-spatial-omics/`](../aacr-2026/topics/single-cell-spatial-omics/index.md) and its [landscape](../aacr-2026/topics/single-cell-spatial-omics/landscape.md).

## AI, computational design, and biomarkers — 15 abstracts

Concentrated in **SS1 — Artificial Intelligence and Design of Immune Modulators**, chaired by **David M. Reese** (Amgen), whose own talk was *"Molecular engineering in the era of artificial intelligence"* (**IA03**), with **Gevorg Grigoryan** (Generate Biomedicines). Upstream of it, **Ed. Session 4** on artificially designing genes and proteins, chaired by **Hani Goodarzi** (UCSF) — *"Generative biology: Reading and writing the language of life."*

Representative abstracts: **A065** (fast prediction of HNSCC treatment response), **C003** (synthetic yeast TCR libraries), **LB-C006** (scalable TCR synthesis with antigen reactivity mapping).

**Note what this theme is and is not.** It is generative protein and immune-modulator *design* — not the clinical-LLM or imaging-foundation-model work that dominates [PSB 2026](../psb-2026/themes.md). Two different meetings, two different meanings of "AI in biomedicine," in the same year. The corpus should keep them distinct.

Corpus fit: [protein-LM explainability](../../talks/fm-to-virtual-cells/adjacent-methods/protein-lm-explainability.md), the [Goodarzi dossier](../../talks/fm-to-virtual-cells/views/people/hani-goodarzi-person.md), and [`aacr-2026/topics/bioinfo-tools/`](../aacr-2026/topics/bioinfo-tools/index.md).

## Neoantigen discovery and cancer vaccines — 17 abstracts

Anchored by Jaffee's opening keynote, *"The Cancer Vaccine Era Has Arrived."* Representative: **B002** (TCR library screened against KRAS G12D/G12V), **A075** (molecular glues expanding the MHC-I immunopeptidome), **LB-B007** (noncanonical "dark genome" neoantigens via PEPMatch/CEDAR), **LB-B009** (sequential shared-TAA then personalized neoantigen vaccination).

The dark-genome abstract is the interesting one: it argues the neoantigen search space has been systematically under-sampled by restricting to canonical ORFs.

## Neuro-psych-immunology — MS8

**The most distinctive programming at the meeting**, and not keyword-countable because it barely has a literature yet.

- **Lili Yang** (UCLA), chair — *"From brain to cancer: Harnessing serotonin and antidepressants for immunotherapy"*
- **Wolf Hervé Fridman** (INSERM U1138) — *"Neuromediators in the tumor microenvironment: GABA modulates tumor immunity and impairs response to immunotherapy"*

Neurotransmitters as tumor-immunity modulators, with an implication that is hard to ignore: commonly prescribed psychiatric drugs may be silently modifying immunotherapy response. If that holds, it is a confounder sitting in every IO trial ever run.

This connects to the neural-immune crosstalk sessions already tracked at [AACR 2026](../aacr-2026/sessions/index.md).

## Cytokine engineering — 18 abstracts

IL-2, IL-12, IL-15, IL-18, and interferon engineering, anchored in MS6. **LB-B010** describes a binding-protein-resistant cytokine receptor agonist; **LB-A010** is the OBX-115 membrane-bound IL-15 program (see [Readouts](readouts.md)). AACR's recap also highlights **Wan Sang Cho** (Stanford) screening roughly **450 synthetic cytokine receptor designs across 14 signaling motifs** — a scale that turns receptor engineering into a search problem.

## The suppressive myeloid compartment — 18 abstracts

MS2, chaired by Marco Colonna with Renato Ostuni (**IA01**). Representative: **A043** (a GATA3-mediated macrophage immunosuppressive program), **B074** (neutrophil extracellular traps), and **LB-A009** / **LB-A011** on neutrophils and S100A9 in **BRCA-carrier breast cancer initiation** — myeloid biology pushed into the pre-malignant window, which is the same territory the [SITC Computational IO series](../sitc-computational-io-2026/index.md) frames as immune interception.

## B cells and tertiary lymphoid structures — 8 abstracts

MS10 on Saturday (Cascone, with Bruno on B cells inside and outside TLS, and Dimberg on inducing TLS in glioma), plus Sautès-Fridman in Ed. 1. **B063** describes **AGB201**, a first-in-class LTβR × EDB bispecific that induces EDB-dependent TLS — turning TLS from a prognostic observation into a therapeutic target.

## The programmed-versus-submitted mismatch

**Microbiome got a full educational session and produced 2 abstracts.** Ed. Session 2 was chaired by Marcel van den Brink with Giorgio Trinchieri and Michael C. Wu — serious people, a full slot — and the submitted science did not follow.

That gap is worth recording. It is the clearest signal in this vault of a field the organizers consider important and the submitting community does not yet, and it is precisely the kind of thing a corpus of conference programs can see that a literature review cannot. Compare the same topic opening the [SITC Computational IO series](../sitc-computational-io-2026/sessions/01-virome-probiotics.md) with a 90-minute three-faculty slot in May 2026 — two societies programming heavily into microbiome IO in the same year.

## Sources

- Abstract census: Crossref API over ISSN 2326-6074, DOIs matching `io2026`, fetched 2026-08-25
- Program: [Wayback snapshots](program.md#sources-wayback-snapshots)
- AACR blog recaps: [Feb 20](https://www.aacr.org/blog/2026/02/20/aacr-io-2026-keynote-highlights-cancer-vaccines-are-here-and-upgrading-t-cells-to-thrive-in-the-tumor-microenvironment/) · [Mar 6](https://www.aacr.org/blog/2026/03/06/highlights-from-aacr-io-2026-breaching-the-tumor-microenvironment-fortress-with-new-car-t-and-chimeras/)
