# Research Article Summary

## Research Question & Novelty
**How do structural mutations alter overall protein conformation and which
regions display the highest variability across diverse protein families?**

Protein Explorer integrates *on‑the‑fly* φ/ψ analysis, RMSD alignment and
3‑D visualisation directly in a web browser — a workflow that normally
requires multiple desktop tools (e.g. PyMOL, Mol*). The novelty lies in the
**combined interactive analytics**: Plotly charts are linked with the NGL
viewer, allowing users to click a Ramachandran region and immediately
highlight residues in 3‑D.

## Literature Review
| Tool | Strengths | Limitations |
|------|-----------|-------------|
| **PyMOL Web** | Mature viewer, scripting | Lacks interactive charts |
| **Mol** | Modern WebGL, large structures | No built‑in φ/ψ statistics |
| **UCSF ChimeraX** | Advanced analysis | Desktop‑only |
| **Protein Explorer** | Combines viewer **+** live analytics in browser | Prototype stage |

## Dataset
*32 PDB entries* spanning enzymes, single‑domain proteins, membrane
receptors and large complexes (see `data/pdb_list.txt`).  
Residue counts range from 46 to 3 900; chain counts — 1 to 59.

## Methods
* **Parsing & metrics** — BioPython (PDB Parser), custom Kabsch RMSD,
  φ/ψ angles via `torsion_dihedral`.  
* **Visualisation** — NGL (3‑D), Plotly (2‑D graphs).  
* **Statistical analysis** — Pandas, Scikit‑learn (PCA, KMeans).

## Results
* **Residue‑count histogram** shows bimodal size distribution.  
* **PCA (2 components)** captures 72 % variance; membrane proteins form
  separate cluster.  
* **KMeans (k = 3)** groups high‑chain complexes apart from single‑domain
  enzymes.  
* **Case study**: R175H mutation in p53 increases global RMSD > 2.3 Å and
  shifts centre‑of‑mass by 4.5 Å, potentially destabilising the DNA‑binding
  loop.

## Discussion
Variability hot‑spots align with flexible loop regions detected in B‑factor
profiles. Membrane proteins display tighter φ/ψ distributions due to
helical transmembrane segments. The integrated workflow reduces manual
tool‑switching and speeds up exploratory analysis.

## Conclusion & Future Work
Protein Explorer demonstrates that full‑stack, browser‑based structural
bioinformatics is feasible. Future steps include MD‑trajectory support and
ML‑driven binding‑pocket prediction.

---
_Full PDF available at [`reports/dataset_analysis.pdf`](../reports/dataset_analysis.pdf)_
