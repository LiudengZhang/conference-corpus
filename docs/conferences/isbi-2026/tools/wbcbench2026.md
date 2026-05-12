# WBCBench2026 — Leukemia Diagnosis Benchmark

**Hematopathology benchmark for white blood cell classification with patient-level test separation — direct leukemia-diagnosis axis testing robust morphological discrimination under severe class imbalance.**

- **Speaker(s) / Authors:** WBCBench2026 organizers (TBD pending challenge-results writeup)
- **Affiliation(s):** TBD (multi-institutional hematopathology consortium typical)
- **Anchor type:** challenge / benchmark
- **Track / day:** ISBI 2026 challenge results session (Sat Apr 11)
- **IEEE Xplore:** TBD (challenge summary paper typically indexed within ~4 weeks post-meeting)
- **Status:** post-meeting

## What it does

WBCBench2026 evaluates fine-grained white blood cell classification on peripheral-blood and bone-marrow smears — the substrate for leukemia and lymphoma diagnosis. The benchmark distinguishes itself by enforcing **patient-level held-out test splits** (preventing the common pitfall where multiple FOVs from the same patient end up across train and test) and by surfacing severe class imbalance characteristic of clinical hematopathology (rare blast morphologies, atypical lymphocytes).

## How it works / methodology

Single-cell crops or full-FOV bone-marrow / peripheral-blood images labeled across WBC morphological categories (neutrophils, lymphocytes, monocytes, eosinophils, basophils, plus blast / atypical categories relevant to leukemia diagnosis). Patient-level separation in train/val/test prevents information leakage. Evaluation uses class-balanced metrics (macro-F1, balanced accuracy) to ensure rare-but-clinically-critical blast classes drive the leaderboard.

## Headline benchmarks

- Patient-level held-out split (specific patient counts TBD pending writeup)
- Class-balanced F1 / balanced accuracy headline metrics
- Top-1 winner + any baseline-beating workshop paper are candidate tool-page entries (TBD post-IEEE-Xplore indexing)

## Where it fits in the corpus

- **AACR 2026:** connects to hematologic-malignancies dossiers; downstream evaluation candidate for general pathology FMs ([CHIEF](../../aacr-2026/topics/bioinfo-tools/tools/chief.md), [UNI](../../aacr-2026/topics/bioinfo-tools/tools/uni.md))
- **MICCAI 2026:** likely COMPAY / MILEX workshop cousin papers
- **ASH 2026 (Dec 12–15):** clinical-deployment counterpart — winning models may resurface as ASH readouts
- **RSNA 2026 / CVPR 2026:** less direct (hematopathology is microscopy-side)

## Notes

Patient-level separation is a methodological best-practice flag worth highlighting — many hematopathology benchmarks pre-2024 used FOV-level splits and over-reported accuracy. WBCBench2026's enforcement is the kind of evaluation-discipline signal worth citing when comparing against older WBC-classification baselines. Watch challenge GitHub for winning-model code drops May–July 2026.
