# Protein Structure Explorer

[![CI Status](https://github.com/katezuu/Protein_Explorer/actions/workflows/ci.yml/badge.svg)](https://github.com/your_username/Protein_Explorer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/katezu/protein-explorer.svg)](https://hub.docker.com/r/katezu/protein-explorer)


## Overview

**Protein Structure Explorer** is a Python-based CLI and web application for:

- Downloading and parsing protein structures from the RCSB PDB.
- Computing basic metrics: residue count, per‐chain counts, amino acid sequences, center of mass (Cα), φ/ψ angles.
- Plotting static 3D scatter (Cα) and Ramachandran plots (φ vs. ψ).
- Comparing two structures by Cα RMSD.
- Serving a simple Flask web interface (with form validation, Bootstrap 5 styling) and REST-like API endpoints.
- Containerizing with Docker and running CI via GitHub Actions (pytest).

---

## Repository Structure


- `explorer.py` — Core functions for parsing PDB, computing metrics, plotting, and RMSD.
- `app.py` — Flask application: routes, form validation, result rendering.
- `templates/` — Jinja2 templates (`index.html`, `result.html`).
- `requirements.txt` — Python dependencies.
- `Dockerfile` — Instructions to build a Docker image.
- `Procfile` — For Heroku/Render to launch Gunicorn.
- `pytest.ini` — pytest configuration.
- `.github/workflows/ci.yml` — GitHub Actions workflow (CI).
- `tests/` — Unit tests (pytest) for both `explorer.py` and `app.py`.
- `LICENSE` — MIT License.

---

## Quick Start (Local / CLI)

1. **Clone or copy** this repository to your local machine.
2. **Navigate** to the project directory:
   ```bash
   cd Protein_Explorer

3. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   flask run
   ```

## Mutation Analysis Features

- `/mutations` form to submit a PDB ID and mutation code.
- `/analyze_mutation` performs simple in-memory modeling of the mutation and displays RMSD and center-of-mass shift.
- REST endpoints `/api/metrics/<pdb_id>` and `/api/mutation_metrics/<pdb_id>/<mutation>` return JSON metrics.

## Interactive Visualization

- Results pages embed the NGL viewer to explore structures in 3D.
- Plotly charts show interactive Cα scatter and Ramachandran plots with zoom and hover capabilities.

## Frontend Dependencies

This project loads the following libraries from CDNs:

- **NGL Viewer** for 3D visualization
- **Plotly.js** for interactive charts
- **Bootstrap 5** for UI styling

## Notebooks & Reports
- 📓 `notebooks/dataset_analysis.ipynb`
- 📄 `reports/dataset_analysis.pdf`
- 💾 `results/dataset_metrics.csv`

