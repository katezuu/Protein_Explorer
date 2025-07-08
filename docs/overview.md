# Protein Explorer

**Interactive web platform for protein structure analysis and visualisation**

## Overview
Protein Explorer lets you upload one or two PDB IDs, computes key structural
metrics (RMSD, φ/ψ angles, centre of mass) and shows the results in the browser
with an interactive 3‑D **NGL viewer** and interactive **Plotly** charts.

## Quick Start

```bash
git clone https://github.com/katezuu/Protein_Explorer.git
cd Protein_Explorer
pip install -r requirements.txt
flask run
```

Or with Docker:

```bash
docker build -t protein-explorer .
docker run -p 5000:5000 protein-explorer
```

## Repository Layout

```text
src/            # Flask & analysis code
templates/      # HTML templates
notebooks/      # Jupyter analysis notebooks
reports/        # PDF reports
results/        # Example CSV/PNG outputs
docs/           # Documentation (this folder)
tests/          # Unit tests & CI
```
