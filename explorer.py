"""Utility wrappers for Protein Explorer."""
from sphinx.util import requests
import requests
from io_utils import (
    download_cif,
    download_pdb,
    download_structure,
    parse_structure,
)
from metrics import (
    compute_center_of_mass,
    compare_structures,
    compute_mutation_rmsd,
    compute_center_of_mass_difference,
)
from plotting import plot_ca_scatter, plot_ramachandran
from mutation import model_mutation

# Re-export helper functions that remained in the original module

from Bio.PDB import PPBuilder, is_aa
from math import degrees


def count_residues(structure) -> tuple[int, dict]:
    chain_counts = {}
    total = 0
    for model in structure:
        for chain in model:
            count = sum(1 for res in chain if is_aa(res))
            chain_counts[chain.id] = count
            total += count
    return total, chain_counts


def get_chain_sequences(structure) -> dict:
    ppb = PPBuilder()
    seq_dict = {}
    for model in structure:
        for chain in model:
            peptides = ppb.build_peptides(chain)
            seq = "".join(str(p.get_sequence()) for p in peptides)
            seq_dict[chain.id] = seq
    return seq_dict


def get_ca_coordinates(structure) -> list:
    return [atom.get_coord().tolist()
            for atom in structure.get_atoms() if atom.get_id() == "CA"]


def get_phi_psi(structure) -> list:
    angles = []
    ppb = PPBuilder()
    for model in structure:
        for chain in model:
            for pp in ppb.build_peptides(chain):
                for phi, psi in pp.get_phi_psi_list():
                    if phi and psi:
                        angles.append((degrees(phi), degrees(psi)))
    return angles


__all__ = [
    "download_cif",
    "download_pdb",
    "download_structure",
    "parse_structure",
    "compute_center_of_mass",
    "compare_structures",
    "compute_mutation_rmsd",
    "compute_center_of_mass_difference",
    "plot_ca_scatter",
    "plot_ramachandran",
    "model_mutation",
    "count_residues",
    "get_chain_sequences",
    "get_ca_coordinates",
    "get_phi_psi",
]


def fetch_uniprot_variants(accession: str) -> list:
    """
    Fetch variant data from UniProt REST API for a given accession.
    Возвращает список словарей вида {'position': <int>}.
    """
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"
    # Выполняем запрос
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    variants = []
    # Ищем все элементы в top‑level features
    for feature in data.get("features", []):
        loc = feature.get("location")
        # Пропускаем, если нет словаря с ключом 'start'
        if not isinstance(loc, dict) or "start" not in loc:
            continue
        pos = loc["start"]
        # Добавляем только если удалось извлечь позицию
        if isinstance(pos, int):
            variants.append({"position": pos})

    return variants
