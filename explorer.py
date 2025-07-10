#!/usr/bin/env python3
"""
explorer.py

Core functions for Protein Structure Explorer:
- download_pdb: retrieves a PDB file from RCSB
- parse_structure: parses PDB into Biopython Structure
- count_residues: counts total residues and per‐chain
- get_chain_sequences: extracts one‐letter amino acid sequences
- compute_center_of_mass: computes average coordinates of Cα atoms
- get_phi_psi: computes φ, ψ dihedral angles (degrees)
- plot_ca_scatter: plots 3D Cα scatter to PNG using Matplotlib
- plot_ramachandran: plots φ vs. ψ scatter
- compare_structures: computes Cα RMSD between two structures
"""

import os

# Use Agg backend so that Matplotlib does not require a display
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from Bio.PDB import PDBList, PDBParser, PPBuilder, is_aa, Superimposer
from math import degrees
from Bio.Data.IUPACData import protein_letters_1to3



def download_pdb(pdb_id: str, out_dir: str = ".") -> str:
    """
    Download a PDB file by its 4‐character ID from RCSB and save it locally.

    Args:
        pdb_id: 4-character PDB identifier (e.g., "1AKE").
        out_dir: Directory in which to save the downloaded PDB.

    Returns:
        Path to the saved PDB file (e.g., "output_dir/1AKE.pdb").

    Raises:
        FileNotFoundError: if PDB is not found on RCSB.
    """
    pdbl = PDBList()
    # retrieve_pdb_file writes something like "pdb1ake.ent" by default
    filepath = pdbl.retrieve_pdb_file(pdb_id, pdir=out_dir, file_format="pdb")
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"PDB {pdb_id} not found on RCSB.")

    # Rename the file to "<pdb_id>.pdb"
    base_name = os.path.basename(filepath)
    new_name = f"{pdb_id}.pdb"
    new_path = os.path.join(out_dir, new_name)

    # Remove if a file with that name already exists
    if os.path.exists(new_path):
        os.remove(new_path)
    os.rename(filepath, new_path)
    return new_path


def parse_structure(file_path: str):
    """
    Parse a PDB file into a Biopython Structure object.

    Args:
        file_path: Path to the local PDB file.

    Returns:
        A Bio.PDB.Structure.Structure object.
    """
    parser = PDBParser(QUIET=True)
    structure_id = os.path.splitext(os.path.basename(file_path))[0]
    structure = parser.get_structure(structure_id, file_path)
    return structure


def count_residues(structure) -> (int, dict):
    """
    Count total amino acid residues and per‐chain counts.

    Args:
        structure: a Bio.PDB.Structure.Structure object.

    Returns:
        total: total number of amino acid residues (int).
        chain_counts: dict mapping chain ID to residue count.
    """
    chain_counts = {}
    total = 0
    for model in structure:
        for chain in model:
            count = 0
            for res in chain:
                if is_aa(res):
                    count += 1
            chain_counts[chain.id] = count
            total += count
    return total, chain_counts


def get_chain_sequences(structure) -> dict:
    """
    Extract one-letter amino acid sequences for each chain.

    Args:
        structure: a Bio.PDB.Structure.Structure object.

    Returns:
        seq_dict: dict mapping chain ID to a sequence string.
    """
    ppb = PPBuilder()
    seq_dict = {}
    for model in structure:
        for chain in model:
            peptides = ppb.build_peptides(chain)
            seq = "".join(str(peptide.get_sequence()) for peptide in peptides)
            seq_dict[chain.id] = seq
    return seq_dict


def compute_center_of_mass(structure) -> np.ndarray:
    """
    Compute approximate center of mass (average Cα coordinates).

    Args:
        structure: a Bio.PDB.Structure.Structure object.

    Returns:
        A numpy array of shape (3,) representing the average x, y, z of all Cα atoms.
        Returns NaNs if no Cα atoms are found.
    """
    coords = []
    for atom in structure.get_atoms():
        if atom.get_id() == "CA":
            coords.append(atom.get_coord())
    coords = np.array(coords)
    if coords.size == 0:
        return np.array([np.nan, np.nan, np.nan])
    return np.mean(coords, axis=0)


def get_ca_coordinates(structure) -> list:
    """Return a list of [x, y, z] for all C-alpha atoms."""
    coords = []
    for atom in structure.get_atoms():
        if atom.get_id() == "CA":
            coords.append(atom.get_coord().tolist())
    return coords


def get_phi_psi(structure) -> list:
    """
    Calculate φ (phi) and ψ (psi) dihedral angles (in degrees) for each residue.

    Args:
        structure: a Bio.PDB.Structure.Structure object.

    Returns:
        angles: a list of tuples [(phi_deg, psi_deg), ...]. Resides without both angles are skipped.
    """
    angles = []
    ppb = PPBuilder()
    for model in structure:
        for chain in model:
            for pp in ppb.build_peptides(chain):
                phi_psi = pp.get_phi_psi_list()
                for phi, psi in phi_psi:
                    if phi and psi:
                        angles.append((degrees(phi), degrees(psi)))
    return angles


def plot_ca_scatter(structure, output_path: str):
    """
    Plot a 3D scatter of all Cα atoms and save as PNG.

Args:
    structure: a Bio.PDB.Structure.Structure object.
    output_path: Path (including filename) to save the PNG.
"""
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    xs, ys, zs = [], [], []
    for atom in structure.get_atoms():
        if atom.get_id() == "CA":
            x, y, z = atom.get_coord()
            xs.append(x)
            ys.append(y)
            zs.append(z)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs, s=10, c="teal", alpha=0.8)
    ax.set_title("C-alpha 3D Scatter")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_ramachandran(angles: list, output_path: str):
    """
    Plot a Ramachandran chart (phi vs. psi) and save as PNG.

    Args:
        angles: list of (phi_deg, psi_deg) tuples.
        output_path: Path (including filename) to save the PNG.
    """
    phis = [a[0] for a in angles]
    psis = [a[1] for a in angles]

    plt.figure()
    plt.scatter(phis, psis, s=5, c="darkorange", alpha=0.7)
    plt.title("Ramachandran Plot")
    plt.xlabel("Phi (°)")
    plt.ylabel("Psi (°)")
    plt.xlim(-180, 180)
    plt.ylim(-180, 180)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def compare_structures(path1: str, path2: str, out_dir: str) -> float:
    """
    Compare two structures by Cα RMSD (superimposed on first chain of each).

    Args:
        path1: Path to the first PDB file.
        path2: Path to the second PDB file.
        out_dir: Directory in which to save the RMSD result text file.

    Returns:
        rmsd (float): Root Mean Square Deviation (Å) after alignment.

    Side Effect:
        Writes a file named "RMSD_<ID1>_<ID2>.txt" under out_dir with one line:
           RMSD between <ID1> and <ID2>: <value> Å
    """
    struct1 = parse_structure(path1)
    struct2 = parse_structure(path2)

    # Use only the first model and the first chain in each structure
    model1 = next(struct1.get_models())
    model2 = next(struct2.get_models())
    chain1_id = next(model1.get_chains()).id
    chain2_id = next(model2.get_chains()).id
    ca1 = [res["CA"] for res in model1[chain1_id] if is_aa(res) and "CA" in res]
    ca2 = [res["CA"] for res in model2[chain2_id] if is_aa(res) and "CA" in res]

    # Trim to the shorter length
    n = min(len(ca1), len(ca2))
    ca1 = ca1[:n]
    ca2 = ca2[:n]

    # Superimpose
    sup = Superimposer()
    sup.set_atoms(ca1, ca2)
    sup.apply(model2.get_atoms())  # transform the second structure

    rmsd_value = sup.rms

    # Write RMSD to a text file
    os.makedirs(out_dir, exist_ok=True)
    id1 = os.path.splitext(os.path.basename(path1))[0]
    id2 = os.path.splitext(os.path.basename(path2))[0]
    txt_filename = f"RMSD_{id1}_{id2}.txt"
    txt_path = os.path.join(out_dir, txt_filename)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"RMSD between {id1} and {id2}: {rmsd_value:.3f} Å\n")

    return rmsd_value


# --- Mutation Analysis Functions ---
import requests
from Bio.PDB.Polypeptide import three_to_index, index_to_three


def fetch_uniprot_variants(accession: str) -> list:
    """Fetch variant data from UniProt REST API for a given accession."""
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch UniProt data: {exc}") from exc

    data = resp.json()
    variants = []
    for feature in data.get("features", []):
        if feature.get("type") == "VARIANT":
            loc = feature.get("location", {})
            pos = loc.get("start")
            desc = feature.get("description", "")
            variant_type = feature.get("ftType", "variant")
            variants.append({
                "position": pos,
                "type": variant_type,
                "description": desc,
                "source": "UniProt",
            })
    return variants


def fetch_clinvar_variants(gene: str) -> list:
    """Fetch variant data from ClinVar for a given gene symbol."""
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=clinvar&retmode=json&term={gene}[gene]"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch ClinVar data: {exc}") from exc

    ids = resp.json().get("esearchresult", {}).get("idlist", [])
    variants = []
    for cid in ids[:5]:  # limit to first few ids for brevity
        summary_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            f"?db=clinvar&id={cid}&retmode=json"
        )
        try:
            sresp = requests.get(summary_url, timeout=10)
            sresp.raise_for_status()
            info = sresp.json()["result"][cid]
            hgvs = info.get("title", "")
            clinsig = info.get("clinical_significance", {}).get("description", "")
            variants.append({
                "hgvs": hgvs,
                "clinical_significance": clinsig,
                "source": "ClinVar",
            })
        except Exception:
            continue
    return variants


def model_mutation(pdb_path: str, mutation: str):
    """Introduce a simple single point mutation and return the mutated structure."""
    struct = parse_structure(pdb_path)
    old = mutation[0]
    new = mutation[-1]
    pos = int(mutation[1:-1])
    for residue in struct.get_residues():
        if residue.id[1] == pos:
            res_letter = new.upper()
            try:
                residue.resname = protein_letters_1to3[res_letter]
            except KeyError:
                raise ValueError(f"Invalid amino‐acid code: {res_letter}")
    return struct


def compute_mutation_rmsd(wt_struct, mut_struct) -> float:
    """Compute CA RMSD between wild type and mutant structures."""
    model1 = next(wt_struct.get_models())
    model2 = next(mut_struct.get_models())
    chain1_id = next(model1.get_chains()).id
    chain2_id = next(model2.get_chains()).id
    ca1 = [res["CA"] for res in model1[chain1_id] if is_aa(res) and "CA" in res]
    ca2 = [res["CA"] for res in model2[chain2_id] if is_aa(res) and "CA" in res]
    n = min(len(ca1), len(ca2))
    ca1 = ca1[:n]
    ca2 = ca2[:n]
    sup = Superimposer()
    sup.set_atoms(ca1, ca2)
    sup.apply(model2.get_atoms())
    return sup.rms


def compute_center_of_mass_difference(wt_struct, mut_struct) -> float:
    """Return Euclidean distance between centers of mass of two structures."""
    com1 = compute_center_of_mass(wt_struct)
    com2 = compute_center_of_mass(mut_struct)
    return float(np.linalg.norm(com1 - com2))
