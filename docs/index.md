---
title: Protein Explorer Documentation
---

# Protein Explorer

**Interactive web platform for protein structure analysis and visualisation**

## Overview
Protein Explorer lets you upload one or two PDB IDs, computes key structural
metrics (RMSD, φ/ψ angles, centre of mass) and shows the results in the browser
with an interactive 3‑D **NGL viewer** and interactive **Plotly** charts.

## Key Features
- Single‑ and dual‑structure analysis with automatic RMSD alignment
- Real‑time φ/ψ Ramachandran plots, Cα scatter and centre‑of‑mass
  visualisation
- Batch analysis notebook for 30 + proteins with PCA and clustering
- Docker container, CI tests and GitHub Pages documentation

## Quick Start

```bash
# Clone & install
git clone https://github.com/katezuu/Protein_Explorer.git
cd Protein_Explorer
pip install -r requirements.txt

# Run the web app
flask run  # opens http://localhost:5000
```

Or use Docker:

```bash
docker build -t protein-explorer .
docker run -p 5000:5000 protein-explorer
```

## Repository Layout

| Folder/File | Purpose |
|-------------|---------|
| `src/` or root `*.py` | Application logic (`app.py`, `explorer.py`) |
| `templates/` | Jinja2 HTML templates |
| `notebooks/` | Jupyter notebooks for dataset analysis |
| `reports/`   | PDF reports (exported notebooks & article) |
| `results/`   | Example CSV/PNG output files |
| `docs/`      | This documentation (published via GitHub Pages) |
| `tests/`     | Pytest unit‑tests & CI workflow |
| `Dockerfile` | Container build definition |

## Notebooks & Reports

* 📓 **Dataset analysis notebook**  
  [`notebooks/dataset_analysis.ipynb`](../notebooks/dataset_analysis.ipynb)

* 📄 **PDF research report**  
  [`reports/dataset_analysis.pdf`](../reports/dataset_analysis.pdf)

* 💾 **Exported metrics CSV**  
  [`results/dataset_metrics.csv`](../notebooks/results/dataset_metrics.csv)

## Documentation Sections
- [Research article summary](research.md)
- [Usability & performance](usability.md)

---
_Last updated: 2025-07-08_
