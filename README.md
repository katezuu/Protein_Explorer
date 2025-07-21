# Protein Structure Explorer

[![CI Status](https://github.com/katezuu/Protein_Explorer/actions/workflows/ci.yml/badge.svg)](https://github.com/your_username/Protein_Explorer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/katezu/protein-explorer.svg)](https://hub.docker.com/r/katezu/protein-explorer)
[![Docs](https://img.shields.io/website?url=https%3A%2F%2Fkatezuu.github.io%2FProtein_Explorer%2F)](https://katezuu.github.io/Protein_Explorer/)

The project was developed for the submission of application documents to POSTECH (Pohang University of Science and Technology) for undergraduate (bachelor's degree) admission.

Protein Structure Explorer is a Flask‑based web application for **interactive 3D visualization**, **structural analysis**, and **mutation modelling** of proteins fetched directly from the PDB or mmCIF archives.

- **3D Viewer** powered by NGL Viewer  
- **Structural stats**: residue counts, center-of-mass, φ/ψ angles  
- **Ramachandran & Cα scatter plots** via Plotly  
- **Mutation simulation** with RMSD & COM-shift metrics  
- **Comparison mode**: compute RMSD between two structures  
![PE GIF.gif](docs/_static/PE%20GIF.gif)

---

## 🔍 Features

- **Fetch PDB/mmCIF** files (with retry & caching)  
- **Parse & analyze** using BioPython  
- **Visualize** via NGL and Plotly  
- **Model point mutations** and highlight them in 3D  
- **API endpoints** for metrics and mutation analysis  

---

## 🛠️ Quick Start

### Local

1. Clone & enter directory  
   ```bash
   git clone https://github.com/katezuu/Protein_Explorer.git
   cd Protein_Explorer
2. Create & activate venv

```bash
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
```
3. Install deps

```bash
pip install -r requirements.txt
```
3. Run

```bash
python app.py
```
Browse http://127.0.0.1:5000

---
## Docker
1. Start Docker Desktop
2. Run
```bash
docker pull katezu/protein-explorer:latest
docker run -d -p 5000:5000 katezu/protein-explorer:latest
```
Browse http://127.0.0.1:5000

---

### 🚦 Testing & CI
```bash
pytest
flake8
```
Continuous integration is set up via GitHub Actions (see .github/workflows/ci.yml).

---
## 📚 Documentation & GitHub Pages
We use MkDocs with the Material theme for our docs site:

```bash
pip install mkdocs mkdocs-material
mkdocs gh-deploy
```

Site lives at:
https://katezuu.github.io/Protein_Explorer/


---
## Research summary
[project‑summary.pdf](paper/project%E2%80%91summary.pdf)

---
## 🤝 Contributing
Fork → branch

Code → tests → commit

PR for review

---
## 📄 License
MIT © Ekaterina Paramonova
