# 🛠️ Installation Guide

## 💻 Local Installation

Clone the repository and set up the virtual environment:

```bash
git clone https://github.com/katezuu/Protein_Explorer.git
cd Protein_Explorer
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python app.py
```


Then open your browser at:


```
http://localhost:5000
```

## 🐳 Docker (Recommended)
Pull and run the Docker image:


```bash
docker pull katezu/protein-explorer:latest
docker run -d -p 5000:5000 katezu/protein-explorer:latest
Then open your browser at:

http://localhost:5000
```
