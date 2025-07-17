# Protein Structure Explorer

[![CI Status](https://github.com/katezuu/Protein_Explorer/actions/workflows/ci.yml/badge.svg)](https://github.com/your_username/Protein_Explorer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/katezu/protein-explorer.svg)](https://hub.docker.com/r/katezu/protein-explorer)
[![Docs](https://img.shields.io/website?url=https%3A%2F%2Fkatezuu.github.io%2FProtein_Explorer%2F)](https://katezuu.github.io/Protein_Explorer/)

**Protein Structure Explorer** is a web-based bioinformatics tool designed to visualize and analyze protein structures directly from the Protein Data Bank (PDB). It allows users to perform detailed structural analysis, visualize protein 3D models, and simulate mutations.

---

## 🚀 Key Features

- **3D Visualization**: Interactive 3D views of protein structures using NGL Viewer.
- **Residue Analysis**: Compute total residues, residues per chain, and center of mass.
- **Mutation Analysis**: Model single-point mutations and calculate structural metrics (RMSD and COM shift).
- **Ramachandran Plot**: Visualize φ (phi) and ψ (psi) angles for structural validation.
- **Comparative Analysis**: Calculate RMSD between two protein structures.
- **Interactive UI**: Easy-to-use web interface built with Flask and Bootstrap 5.

---

## 🛠️ Technologies Used

- **Backend**: Python, Flask, BioPython, NumPy, Matplotlib.
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript, NGL Viewer, Plotly.
- **DevOps**: Docker, GitHub Actions for CI/CD, Heroku/Render deployment ready.

---

## ⚙️ Installation and Usage

### Local Development

1. **Clone this repository**:
```bash
git clone https://github.com/katezuu/Protein_Explorer.git
cd Protein_Explorer
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

5. **Open your browser** and navigate to:
```
http://127.0.0.1:5000
```

### Docker (Recommended)

1. **Pull the latest Docker image**:
```bash
docker pull katezu/protein-explorer:latest
```

2. **Run with Docker**:
```bash
docker run -d -p 5000:5000 katezu/protein-explorer:latest
```

3. **Access via browser**:
```
http://localhost:5000
```

---

## 🚧 Testing

Run unit tests using:
```bash
pytest
```

---

## 📦 Deployment

This application is ready for deployment on platforms like **Heroku** or **Render**.

Example Heroku deployment commands:

```bash
heroku create protein-explorer-yourname
git push heroku main
heroku ps:scale web=1
heroku open
```

---

## 📖 Documentation

Detailed documentation is available in the [docs](./docs) folder.

---

## ✅ Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Create a new Pull Request.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.