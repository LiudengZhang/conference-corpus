# MPI Low Concentration Reconstruction Challenge — ISBI 2026

**Field-free-line magnetic particle imaging reconstruction at low tracer concentrations — the clinical-translation bottleneck for MPI, with explicit oncology and cardiovascular imaging applications flagged in the challenge description.**

- **Speaker(s) / Authors:** MPI Low Concentration Challenge organizers (TBD pending challenge-results writeup)
- **Affiliation(s):** TBD (MPI community is centered around Lübeck / Würzburg / Berkeley groups)
- **Anchor type:** challenge
- **Track / day:** ISBI 2026 challenge results session (Sat Apr 11)
- **IEEE Xplore:** TBD (challenge summary paper typically indexed within ~4 weeks post-meeting)
- **Status:** post-meeting

## What it does

Magnetic Particle Imaging (MPI) is an emerging tracer-based molecular imaging modality that directly visualizes the spatial distribution of superparamagnetic iron oxide nanoparticles with zero ionizing radiation and zero background signal from tissue. Clinical translation has been gated by reconstruction quality at low tracer concentrations — the regime needed for both oncology (tumor-specific tracer payloads, sentinel-lymph-node mapping) and cardiovascular imaging. This challenge benchmarks reconstruction algorithms specifically at the low-concentration regime using field-free-line MPI (FFL-MPI) setups.

## How it works / methodology

Participants submit reconstruction algorithms — classical (Kaczmarz / regularized least squares), model-based with learned priors, or end-to-end deep learning — that map raw FFL-MPI measurement data to tracer concentration images. Evaluation focuses on image quality (PSNR / SSIM against high-concentration reference reconstructions), spatial resolution recovery, and quantitative concentration accuracy in the low-tracer regime.

## Headline benchmarks

- FFL-MPI dataset (specific phantom / in-vivo composition TBD)
- PSNR / SSIM / concentration-quantification metrics; top-1 reconstruction algorithm and any methods paper introducing a new MPI DL prior are candidate tool-page entries
- Specific top-1 numbers TBD pending challenge writeup

## Where it fits in the corpus

- **AACR 2026:** indirect — molecular imaging axis; MPI is not yet in AACR clinical dossiers but is a candidate emerging modality for tumor-targeted tracer studies
- **MICCAI 2026:** MPI is ISBI-overweighted; MICCAI cousin coverage is sparse
- **RSNA 2026:** clinical-translation watch — if any MPI system reaches first-in-human at an oncology indication, RSNA is the deployment venue
- **CVPR 2026:** not direct — inverse-problems methodology could cross-pollinate via CVPR FMV / generative-modeling workshops

## Notes

ISBI is the home venue for MPI methods (MICCAI underweights this modality entirely). The explicit oncology translation goal in the challenge framing is the load-bearing reason this entry sits in the cancer-relevant filter — MPI's value proposition for cancer imaging is tumor-targeted tracer accumulation at concentrations below current reconstruction-quality thresholds, which is exactly what this challenge attacks. Watch for TBME Special Section invitation of the top methods paper.
