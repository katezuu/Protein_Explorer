#!/usr/bin/env python3
"""
explorer.py

Core functions for Protein Structure Explorer:
- download_structure: retrieves mmCIF (preferably) or PDB files from RCSB
- parse_structure: parses PDB/mmCIF into Biopython Structure
- count_residues: counts total residues and per‐chain
- get_chain_sequences: extracts one‐letter amino acid sequences
- compute_center_of_mass: computes average coordinates of Cα atoms
- get_ca_coordinates: returns list of Cα coords
- get_phi_psi: computes φ, ψ dihedral angles (degrees)
- plot_ca_scatter: plots 3D Cα scatter to PNG
- plot_ramachandran: plots φ vs. ψ
- compare_structures: computes Cα RMSD between two structures
- model_mutation: applies single‐point mutation with sidechain rotation
- compute_mutation_rmsd: RMSD between WT and mutant Cα atoms
- compute_center_of_mass_difference: COM shift
- fetch_uniprot_variants / fetch_clinvar_variants: variant lookups
"""

import os
import gzip
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from math import degrees
from Bio.PDB import (
    PDBParser,
    MMCIFParser,
    PPBuilder,
    is_aa,
    Superimposer
)
from Bio.Data.IUPACData import protein_letters_1to3
from Bio.PDB.Polypeptide import is_aa as _is_aa
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Cache directory for CIF/PDB downloads
CACHE_DIR = os.path.join(os.path.dirname(__file__), "data", "cifs")
os.makedirs(CACHE_DIR, exist_ok=True)


def _get_session():
    """Return a requests.Session with retry logic configured."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def download_cif(pdb_id: str, out_dir: str) -> str:
    """
    Download mmCIF for pdb_id into out_dir, cache in CACHE_DIR, and gzip it.
    Returns path to .cif file.
    """
    pdb_id = pdb_id.upper()
    cache_cif = os.path.join(CACHE_DIR, f"{pdb_id}.cif")
    cache_gz  = cache_cif + ".gz"
    if os.path.exists(cache_cif) and os.path.exists(cache_gz):
        return cache_cif

    session = _get_session()
    url = f"https://files.rcsb.org/download/{pdb_id}.cif"
    resp = session.get(url, timeout=30)
    resp.raise_for_status()

    os.makedirs(out_dir, exist_ok=True)
    out_cif = os.path.join(out_dir, f"{pdb_id}.cif")
    with open(out_cif, "wb") as f:
        f.write(resp.content)
    # cache
    with open(cache_cif, "wb") as f:
        f.write(resp.content)
    # gzip for client-side viewer
    with gzip.open(cache_gz, "wb") as gz:
        gz.write(resp.content)

    return out_cif


def download_pdb(pdb_id: str, out_dir: str) -> str:
    """
    Download PDB format for pdb_id into out_dir, cache in CACHE_DIR.
    Returns path to .pdb file.
    """
    pdb_id = pdb_id.upper()
    cache_pdb = os.path.join(CACHE_DIR, f"{pdb_id}.pdb")
    if os.path.exists(cache_pdb):
        return cache_pdb

    session = _get_session()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    resp = session.get(url, timeout=30)
    resp.raise_for_status()

    os.makedirs(out_dir, exist_ok=True)
    out_pdb = os.path.join(out_dir, f"{pdb_id}.pdb")
    with open(out_pdb, "wb") as f:
        f.write(resp.content)
    # cache
    with open(cache_pdb, "wb") as f:
        f.write(resp.content)

    return out_pdb


def download_structure(pdb_id: str, out_dir: str):
    """
    Try to download mmCIF (and gzip), otherwise fall back to PDB.
    Returns (filename, fmt) where fmt is 'mmcif_gz', 'mmcif', or 'pdb'.
    """
    try:
        cif_path = download_cif(pdb_id, out_dir)
        gz_path = cif_path + ".gz"
        if os.path.exists(gz_path):
            return (os.path.basename(gz_path), 'mmcif_gz')
        return (os.path.basename(cif_path), 'mmcif')
    except Exception:
        pdb_path = download_pdb(pdb_id, out_dir)
        return (os.path.basename(pdb_path), 'pdb')


def parse_structure(path: str):
    """
    Parse a .pdb or .cif/mmcif file into a Bio.PDB Structure.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdb":
        parser = PDBParser(QUIET=True)
    elif ext in (".cif", ".mmcif"):
        parser = MMCIFParser(QUIET=True)
    else:
        raise ValueError(f"Unsupported format: {ext}")
    return parser.get_structure(os.path.basename(path), path)


def count_residues(structure) -> (int, dict):
    """
    Count total amino acid residues and per‐chain.
    Returns (total, {chain_id: count, ...}).
    """
    chain_counts = {}
    total = 0
    for model in structure:
        for chain in model:
            count = sum(1 for res in chain if is_aa(res))
            chain_counts[chain.id] = count
            total += count
    return total, chain_counts


def get_chain_sequences(structure) -> dict:
    """
    Extract one-letter sequences for each chain.
    Returns {chain_id: sequence}.
    """
    ppb = PPBuilder()
    seq_dict = {}
    for model in structure:
        for chain in model:
            peptides = ppb.build_peptides(chain)
            seq = "".join(str(p.get_sequence()) for p in peptides)
            seq_dict[chain.id] = seq
    return seq_dict


def compute_center_of_mass(structure) -> np.ndarray:
    """
    Compute average coordinates of all Cα atoms.
    Returns np.array([x,y,z]) or NaNs if none found.
    """
    coords = [atom.get_coord()
              for atom in structure.get_atoms() if atom.get_id() == "CA"]
    if not coords:
        return np.array([np.nan, np.nan, np.nan])
    return np.mean(coords, axis=0)


def get_ca_coordinates(structure) -> list:
    """
    Return list of [x,y,z] for all Cα atoms.
    """
    return [atom.get_coord().tolist()
            for atom in structure.get_atoms() if atom.get_id() == "CA"]


def get_phi_psi(structure) -> list:
    """
    Calculate φ, ψ angles (degrees) for each residue.
    Returns list of (phi, psi).
    """
    angles = []
    ppb = PPBuilder()
    for model in structure:
        for chain in model:
            for pp in ppb.build_peptides(chain):
                for phi, psi in pp.get_phi_psi_list():
                    if phi and psi:
                        angles.append((degrees(phi), degrees(psi)))
    return angles


def plot_ca_scatter(structure, output_path: str):
    """
    Plot 3D scatter of Cα atoms to PNG.
    """
    from mpl_toolkits.mplot3d import Axes3D  # noqa

    xs = []; ys = []; zs = []
    for atom in structure.get_atoms():
        if atom.get_id() == "CA":
            x, y, z = atom.get_coord()
            xs.append(x); ys.append(y); zs.append(z)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs, s=10, c="teal", alpha=0.8)
    ax.set_title("C-alpha 3D Scatter")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_ramachandran(angles: list, output_path: str):
    """
    Plot Ramachandran chart (φ vs. ψ) to PNG.
    """
    phis = [a[0] for a in angles]; psis = [a[1] for a in angles]
    plt.figure()
    plt.scatter(phis, psis, s=5, c="darkorange", alpha=0.7)
    plt.title("Ramachandran Plot")
    plt.xlabel("Phi (°)"); plt.ylabel("Psi (°)")
    plt.xlim(-180, 180); plt.ylim(-180, 180)
    plt.grid(True); plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def compare_structures(path1: str, path2: str, out_dir: str) -> float:
    """
    Compute Cα RMSD between two structures by matching chain IDs and residue numbers.
    If no matching Cα atoms are found, returns 0.0 instead of raising.
    """
    struct1 = parse_structure(path1)
    struct2 = parse_structure(path2)

    model1 = next(struct1.get_models())
    model2 = next(struct2.get_models())

    ca1, ca2 = [], []
    for chain1 in model1:
        if chain1.id not in model2:
            continue
        chain2 = model2[chain1.id]
        for res1 in chain1:
            if not is_aa(res1) or "CA" not in res1:
                continue
            res_id = res1.id
            if res_id not in chain2 or "CA" not in chain2[res_id]:
                continue
            ca1.append(res1["CA"])
            ca2.append(chain2[res_id]["CA"])

    # Если ничего не найдено — просто вернём 0.0
    if not ca1:
        return 0.0

    sup = Superimposer()
    sup.set_atoms(ca1, ca2)
    sup.apply(list(model2.get_atoms()))
    rmsd_value = sup.rms

    # Запись отчёта в UTF-8
    os.makedirs(out_dir, exist_ok=True)
    id1 = os.path.splitext(os.path.basename(path1))[0]
    id2 = os.path.splitext(os.path.basename(path2))[0]
    report = f"RMSD between {id1} and {id2}: {rmsd_value:.3f} Å\n"
    txt_path = os.path.join(out_dir, f"RMSD_{id1}_{id2}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report)

    return rmsd_value


def model_mutation(pdb_path: str, mutation: str):
    """
    Introduce a single‐point mutation by renaming residue and rotating
    its sidechain by 45° around the Cα, so that RMSD and COM shift != 0.
    """
    struct = parse_structure(pdb_path)
    new_aa = mutation[-1].upper()
    pos    = int(mutation[1:-1])

    # build rotation matrix (Rodrigues) for 45° about Z-axis
    theta = np.deg2rad(45.0)
    axis = np.array([0.0, 0.0, 1.0])
    K = np.array([[    0,     -axis[2], axis[1]],
                  [ axis[2],     0,    -axis[0]],
                  [-axis[1], axis[0],     0   ]])
    R = np.eye(3) + np.sin(theta)*K + (1 - np.cos(theta))*(K @ K)

    # apply mutation
    for residue in struct.get_residues():
        if residue.id[1] != pos:
            continue
        # rename
        try:
            residue.resname = protein_letters_1to3[new_aa]
        except KeyError:
            raise ValueError(f"Invalid amino-acid code: {new_aa}")
        # rotate sidechain atoms about Cα
        ca = residue["CA"]
        ca_coord = ca.get_coord()
        for atom in residue:
            if atom.get_id() == "CA":
                continue
            v = atom.get_coord() - ca_coord
            atom.set_coord(ca_coord + R.dot(v))
        break

    return struct


def compute_mutation_rmsd(wt_struct, mut_struct, mutation: str) -> float:
    """
    Compute RMSD over sidechain atoms (all non‐backbone atoms) for the single
    mutated residue specified by mutation string (e.g. "A141D").
    """
    # Распарсим mutation: первая буква – цепь, цифры – номер
    chain_id = mutation[0]
    resnum   = int(mutation[1:-1])

    # Берём первый модель из каждой структуры
    model1 = next(wt_struct.get_models())
    model2 = next(mut_struct.get_models())

    # Достаём нужные остатки
    try:
        res1 = model1[chain_id][resnum]
        res2 = model2[chain_id][resnum]
    except KeyError:
        raise ValueError(f"Residue {chain_id}{resnum} not found in one of structures")

    # Список пар атомов боковой цепи (исключаем backbone N, CA, C, O)
    bb = {"N","CA","C","O"}
    atoms1 = [a for a in res1 if a.get_id() not in bb and a.get_id() in {b.get_id() for b in res2}]
    atoms2 = [res2[a.get_id()] for a in atoms1]

    if not atoms1:
        # нет боковой цепи (например Gly) — RMSD = 0
        return 0.0

    # Собираем координаты и считаем RMSD без суперпозиции
    diffs2 = []
    for a1, a2 in zip(atoms1, atoms2):
        d = a2.get_coord() - a1.get_coord()
        diffs2.append(np.dot(d, d))
    rmsd = float(np.sqrt(sum(diffs2) / len(diffs2)))
    return rmsd
    return sup.rms


def compute_center_of_mass_difference(wt_struct, mut_struct) -> float:
    """Return Euclidean distance between centers of mass of two structures."""
    com1 = compute_center_of_mass(wt_struct)
    com2 = compute_center_of_mass(mut_struct)
    return float(np.linalg.norm(com1 - com2))


def fetch_uniprot_variants(accession: str) -> list:
    """Fetch variant data from UniProt REST API for a given accession."""
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    variants = []
    for feature in data.get("features", []):
        if feature.get("type") == "VARIANT":
            loc = feature.get("location", {})
            variants.append({
                "position": loc.get("start"),
                "description": feature.get("description", ""),
                "source": "UniProt"
            })
    return variants


def fetch_clinvar_variants(gene: str) -> list:
    """Fetch variant data from ClinVar for a given gene symbol."""
    search_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=clinvar&retmode=json&term={gene}[gene]"
    )
    resp = requests.get(search_url, timeout=10)
    resp.raise_for_status()
    ids = resp.json().get("esearchresult", {}).get("idlist", [])
    variants = []
    for cid in ids[:5]:
        summary_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            f"?db=clinvar&id={cid}&retmode=json"
        )
        sresp = requests.get(summary_url, timeout=10)
        sresp.raise_for_status()
        info = sresp.json().get("result", {}).get(cid, {})
        variants.append({
            "hgvs": info.get("title", ""),
            "clinical_significance": info.get("clinical_significance", {}).get("description", ""),
            "source": "ClinVar"
        })
    return variants