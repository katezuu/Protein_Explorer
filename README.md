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

