"""Utility wrappers for Protein Explorer."""
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
    """
    FIX: Changed condition from 'if phi and
    psi:' to 'if phi is not None and psi is not None:'
    to correctly handle zero-degree
    angles (which are valid but evaluate to False)
    """
    angles = []
    ppb = PPBuilder()
    for model in structure:
        for chain in model:
            for pp in ppb.build_peptides(chain):
                for phi, psi in pp.get_phi_psi_list():
                    # FIX: Properly check for None instead of truthiness
                    if phi is not None and psi is not None:
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
    Returns list of dicts with key 'position'.

    FIX: Added try-except block for robust error handling
    """
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        variants = []
        for feature in data.get("features", []):
            loc = feature.get("location", {})
            pos = loc.get("start")
            if isinstance(pos, int):
                variants.append({"position": pos})
        return variants

    except requests.exceptions.RequestException as e:
        # FIX: Handle network errors gracefully
        print(f"Warning: Failed to fetch "
              f"UniProt variants for {accession}: {e}")
        return []
    except (KeyError, ValueError) as e:
        # FIX: Handle JSON parsing errors
        print(f"Warning: Failed to parse "
              f"UniProt response for {accession}: {e}")
        return []
