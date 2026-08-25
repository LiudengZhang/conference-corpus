# GCC2026 — Community program

Everything at [GCC2026](index.md) outside the [talk sessions](talks/index.md): Birds-of-a-Feather, SIGs, training, and the two-day CoFest. For a community-run platform this is where much of the real work happened, and it is unusually well documented.

## Birds-of-a-Feather

Ten BoFs across two blocks, five in parallel each time. Full list from the [BoF page](https://galaxyproject.org/events/gcc2026/bofs/).

### Monday, 17:00–18:00

| BoF | Leads | Room |
|---|---|---|
| **Galaxy as the Substrate for Agent-driven Science** | Dannon Baker, Anton Nekrutenko | Amphitheater A |
| Federation of instances: atypical multi-HPC integration. Is Pulsar the solution? | Vlad Visan, Marie Jossé, Yvan Le Bras, Samuel Keuchkerian, Martin Carrère, Sanjay Srikakulam | Amph. B |
| **Keeping pace with best practices in single-cell and spatial omics in Galaxy** | Kevin Rue-Albrecht, Marisa Loach | Espace doc |
| How to build and structure one's community: the quid of overlapping communities | Marie Jossé, Beatriz Serrano-Solano, Yvan Le Bras, Jérôme Detoc, Samuel Keuchkerian | Cafeteria |
| Access and Identity — Now that I know who you are, what do I do? | Galaxy Australia team | Entrance hall |

The agent BoF covered driving Galaxy through Claude Code, Codex, `galaxy-mcp`, Loom, and Orbit. The single-cell BoF was anchored on the **BioFAIR Pathfinder** project and Seurat / Bioconductor / Scanpy interoperability — see [Themes](themes.md#single-cell-and-spatial-omics-in-galaxy).

### Wednesday, 17:15–18:30

| BoF | Leads | Room |
|---|---|---|
| At the edge of the Galaxy, the lonely life of a (small scale) local Galaxy server admin | Hans-Rudolf Hotz, Lucille Delisle | — |
| Community Discussion on Open Source Approaches for Automated Galaxy Tool Generation | Daniel Blankenberg | Amph. B |
| Where does Galaxy's security responsibility end and yours begin? | Martin Carrère, Nate Coraor | Cafeteria |
| IDC (Intergalactic Data Commission / reference data) | Matthias Bernt | Salle doc |
| Galaxy Release Process and Test Coverage Gaps | Aysam Guerler | — |

## Special Interest Groups

Monday's **Overview of Galaxy SIGs** session covered the full directory: Computational Chemistry, Earth, Ecology, Genome Annotation, Materials Science, Microbiology, Public Health, Digital Humanities, Machine Learning, Metabolomics, Proteomics, **Single-cell & sPatial Omics (SPOC)**, and Image Analysis. Directory: [galaxyproject.org/community/sig/](https://galaxyproject.org/community/sig/).

Two SIGs published dedicated GCC2026 recaps.

### Machine Learning SIG

Led by **Anup Kumar**, with Michelle Savage, Paulo Morais, Dannon Baker, and Jeremy Goecks. GCC2026 contributions:

- Poster *AI/ML tools in Galaxy* — [Zenodo 10.5281/zenodo.21133087](https://doi.org/10.5281/zenodo.21133087)
- ELIXIR BioHackathon Project 13 talk, *Bridging DOME, BioAIrepo, BioModels and Galaxy* — [project page](https://github.com/elixir-europe/BioHackathon-projects-2026/blob/main/13.md)
- The **Machine Learning for Genomics** training session (Friday), delivered by Michelle Savage and Anup Kumar using the [**GLEAM Image Learner** GTN tutorial](https://training.galaxyproject.org/training-material/topics/statistics/tutorials/image_learner/tutorial.html) — biomedical image classification covering dataset splitting, pretrained backbones, and evaluation on imbalanced medical data
- CoFest PR to [`galaxyproject/galaxy` #23027](https://github.com/galaxyproject/galaxy/pull/23027) — validating and displaying reference URLs in LLM responses

Recap: <https://galaxyproject.org/news/2026-07-01-gcc-ml-2026/>

### microGalaxy SIG (Microbiology)

One of the project's most developed communities. The **Microbiology Galaxy Lab** ships **315+ tools and 115+ curated workflows**, deployed on `microbiology.usegalaxy.eu`, `.fr`, `.org`, and `.org.au`, with 30+ training events over five years. At GCC2026: multiple talks and posters, the reference-data BoF, and CoDex development during CoFest.

Recap: <https://galaxyproject.org/news/2026-07-13-gcc-microbiome-2026/>

## Training

Thursday and Friday, 09:00–12:00, three parallel tracks each morning in rooms A128–A130.

| Day | Tracks |
|---|---|
| **Thu Jun 25** | New and Experienced User Walkthroughs · Tool Wrapping · Getting Ready for Galaxy Development in CoFest |
| **Fri Jun 26** | Developers Do Bioinformatics · Earth Science & Ecology · **Machine Learning for Genomics** |

**Instructor names are not published** for five of the six sessions. Only the ML session's instructors are known (Savage and Kumar), via the ML SIG recap.

## CoFest

Thursday and Friday afternoons, 13:00–18:00. **16–19 projects, ~85+ contributors.** Full outcomes: <https://galaxyproject.org/news/2026-07-20-gcc2026-cofest-outcomes/>

| Project | Lead | Notes |
|---|---|---|
| Driving Galaxy with Agents | Dannon Baker | 7 participants → [`galaxy-mcp` PR #89](https://github.com/galaxyproject/galaxy-mcp/pull/89) |
| AI agent auto-wrap tools | Enis Afgan | |
| Galaxy CoDex | Solenne Correard | 6 participants |
| Molstar / structural biology | Finn Beruldsen | |
| GTN tool-review materials | Mélanie Pétéra | |
| GTN admin training + TPV debugging | Paul De Geest | [`total-perspective-vortex` PR #198](https://github.com/galaxyproject/total-perspective-vortex/pull/198) |
| Pangenomics | Anton Nekrutenko | |
| File sources / OpenSILEX | Polina Polunina | |
| **Bioconductor tools + single-cell GTN** | Kevin Rue-Albrecht | |
| Arts & humanities | Eamonn Bell | |
| Modernizing Pulsar DRMAA | Matthias Bernt | |
| Time-based quotas, pgcleanup | Charles Coulombe | |
| Galaxy on Kubernetes | Keith Suderman | |
| CVMFS reference genomes | Sveinung Gundersen | |
| Tool wrapping for public health | Peter van Heusden | |
| Metabolomics / EIRENE | Helge Hecht | |
| Ecology tools | Yvan Le Bras | |
| Grow the GTN | Saskia Hiltemann | |
| Bring workflow to IWC | Lucille Delisle | |

Also referenced: `galaxyproject/galaxy_codex` PRs #690, #697, #710, #711, #712.

## Slides and posters

**Decentralized — there is no single GCC2026 slide repository.** Three venues are in use, which means a complete harvest requires all three.

**HAL** (13 GCC2026 deposits confirmed; URL pattern `https://hal.science/<halId>`): `hal-05693116` *Galaxy + France = ❤️* · `hal-05685741` *FAIRyMAGs* · `hal-05693236` *Microbiology Galaxy Lab* · `hal-05693206` *CoDex* · `hal-05699789` *Biodiversity Genomics Galaxy Lab* · `hal-05694938` *Galaxy-BioProd* · `hal-05680506` *W4M boat* · `hal-05682190` *Small Scale Admins* · `hal-05630495` *Synthetic Biology in Galaxy* · `hal-05713233` *Experimental protocols / FAIR* · `hal-05688981` *sncRNA workflow suites* · `hal-05677408` *OSUG Galaxy customisation* · `hal-05646530` *First-time Galaxy tool integration*

**F1000Research** — mirrors of the French deposits: [slides 15-1124](https://f1000research.com/slides/15-1124) (*Galaxy + France = ❤️*, Batut B, Galaxy France Working Group, Le Corguillé G, Bretaudeau A); posters [15-1114](https://f1000research.com/posters/15-1114) (Microbiology Galaxy Lab), [15-1115](https://f1000research.com/posters/15-1115) (CoDex), [15-1166](https://f1000research.com/posters/15-1166) (Biodiversity Genomics Galaxy Lab), [15-1175](https://f1000research.com/posters/15-1175) (Galaxy-BioProd). *Note: f1000research.com returns HTTP 403 to automated fetchers; use a browser.*

**Zenodo** — ad-hoc, with **no GCC2026 community** (a `q=GCC2026` API search returns zero): [record 21128145](https://zenodo.org/records/21128145) (*FAIRyMAGs*) and [10.5281/zenodo.21133087](https://doi.org/10.5281/zenodo.21133087) (*AI/ML tools in Galaxy*).

## Sources

- BoFs: <https://galaxyproject.org/events/gcc2026/bofs/>
- Training: <https://galaxyproject.org/events/gcc2026/training/>
- CoFest outcomes: <https://galaxyproject.org/news/2026-07-20-gcc2026-cofest-outcomes/>
- SIG directory: <https://galaxyproject.org/community/sig/>
- All fetched 2026-08-25.
