# Protein Explorer <!-- omit in toc -->

Interactive web platform for **analysis and 3-D visualisation of PDB structures**  
_(Flask • Biopython • NGL • Plotly)_  

[Live demo ↗](../) • [Research article ↗](research.md)

## Table of contents
1. [Overview](#overview)  
2. [Quick start](#quick-start)  
3. [Installation](#installation)  
4. [Project layout](#project-layout)  
5. [Notebooks & Reports](#notebooks--reports)  
6. [Contributing](#contributing)  

---

## Overview
Protein Explorer lets you **upload or fetch PDB entries**, calculate key
metrics (RMSD, φ/ψ angles, centre of mass), and inspect structures
directly in the browser via NGL and Plotly widgets.

Main features  
- One-click download of PDB IDs (single or pair)  
- Real-time φ/ψ and C-α scatter plots (Plotly)  
- RMSD alignment and heat-map export  
- Containerised deployment (Docker)  
- Jupyter notebook for large-scale dataset analysis  
- Unit-tested core (`pytest`, CI workflow)

## Quick start

```bash
# clone & install
git clone https://github.com/katezuu/Protein_Explorer.git
cd Protein_Explorer
pip install -r requirements.txt

# run locally
flask run  # open http://localhost:5000
