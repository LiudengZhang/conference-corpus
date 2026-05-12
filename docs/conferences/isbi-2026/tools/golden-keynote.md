# Medical Imaging Learning — Polina Golland (MIT CSAIL)

**ISBI 2026 plenary keynote on statistical methods, MRI reconstruction, and image registration for medical imaging — the methods-side foundation for downstream cancer-MRI workflows even though the keynote itself is method-axis, not oncology-direct.**

- **Speaker(s) / Authors:** Polina Golland
- **Affiliation(s):** MIT CSAIL (Computer Science and Artificial Intelligence Laboratory)
- **Anchor type:** keynote
- **Track / day:** ISBI 2026 main plenary (day TBD — Thu Apr 9 or Fri Apr 10)
- **IEEE Xplore:** TBD (keynote — no Xplore paper)
- **Status:** post-meeting

## What it does

Golland's keynote covers three of MIT CSAIL's long-running medical imaging axes: (1) accelerated MRI reconstruction via learned priors, (2) deformable image registration with learning-based approaches (the VoxelMorph line), (3) statistical methods for population-level imaging analyses. These methods are the substrate that downstream cancer-imaging workflows depend on — cancer-MRI rapid-reconstruction pipelines, tumor tracking via registration, population-level radiomics studies.

## How it works / methodology

The Golland-lab pattern is rigorous statistical-method development plus open-source reference implementations: VoxelMorph (learning-based registration) became the de-facto baseline for deformable registration; learned priors for MRI reconstruction (compressed-sensing-with-learning hybrids) bridge classical inverse-problem theory and modern deep learning. Methods emphasize sample efficiency, interpretability, and demonstrable behavior under distribution shift — qualities that matter when downstream use is clinical.

## Headline benchmarks

TBD — keynote-level synthesis; the published Golland-lab work (VoxelMorph, learned MRI reconstruction priors) remains the citation anchor. ISBI 2026 keynote likely surfaced an update or new direction; specific deltas not in program-notes.

## Where it fits in the corpus

- **AACR 2026:** indirect — methods feed cancer-MRI workflows but no direct pathology-FM crosswalk
- **MICCAI 2026:** strong methods-axis sibling — Golland-lab work consistently appears at MICCAI main proceedings; cousin papers likely Sep 27–Oct 1
- **RSNA 2026:** indirect — VoxelMorph and learned MR reconstruction underlie many clinical-translation systems shown at RSNA
- **CVPR 2026:** Golland-lab work bridges to CVPR's generative-modeling and inverse-problems tracks

## Notes

Keynote-axis page only — no tool artifact directly attached. Watch for any ISBI 2026 main-proceedings paper from Golland-lab students that releases a named model, which would warrant a separate tool page. The keynote serves as a methodological anchor in the vault for "where the ISBI methods axis sits relative to cancer-imaging downstream."
