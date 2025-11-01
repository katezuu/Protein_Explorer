import os
import copy
import numpy as np
from Bio.PDB import Superimposer, is_aa
from io_utils import parse_structure

# FIX: Added atomic mass lookup table for mass-weighted COM
ATOMIC_MASSES = {
    'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'S': 32.065, 'P': 30.974, 'F': 18.998, 'CL': 35.453,
    'BR': 79.904, 'I': 126.904, 'SE': 78.96, 'FE': 55.845,
    'ZN': 65.38, 'MG': 24.305, 'CA': 40.078, 'NA': 22.990,
    'K': 39.098, 'MN': 54.938, 'CU': 63.546, 'NI': 58.693,
}


def get_atomic_mass(element: str) -> float:
    """
    Return atomic mass for an element symbol.
    FIX: Handles unknown elements with a default mass of 12.0
    """
    element_upper = element.upper().strip()
    return ATOMIC_MASSES.get(element_upper, 12.0)


def compute_center_of_mass(structure) -> np.ndarray:
    """
    FIX: Compute mass-weighted center of mass instead of geometric centroid
    """
    coords: list[np.ndarray] = []
    masses: list[float] = []

    for atom in structure.get_atoms():
        coords.append(atom.get_coord())
        # FIX: Use actual atomic masses based on element
        element = atom.element if hasattr(atom, 'element') else 'C'
        masses.append(get_atomic_mass(element))

    if not coords:
        return np.array([np.nan, np.nan, np.nan])

    coords = np.array(coords)
    masses = np.array(masses)

    # FIX: Mass-weighted average instead of simple mean
    com = np.average(coords, axis=0, weights=masses)
    return com


def compare_structures(path1: str, path2: str, out_dir: str) -> float:
    """
    FIX: Use deep copy to avoid
    mutating original structure during superposition
    """
    struct1 = parse_structure(path1)
    struct2 = parse_structure(path2)

    model1 = next(struct1.get_models())
    # FIX: Create a deep copy to prevent mutation of original structure
    model2 = copy.deepcopy(next(struct2.get_models()))

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

    if not ca1:
        return 0.0

    sup = Superimposer()
    sup.set_atoms(ca1, ca2)
    # FIX: Apply superposition to the copy, not the original
    sup.apply(list(model2.get_atoms()))
    rmsd_value = sup.rms

    os.makedirs(out_dir, exist_ok=True)
    id1 = os.path.splitext(os.path.basename(path1))[0]
    id2 = os.path.splitext(os.path.basename(path2))[0]
    txt_path = os.path.join(out_dir, f"RMSD_{id1}_{id2}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"RMSD between {id1} and {id2}: {rmsd_value:.3f} Å\n")

    return rmsd_value


def compute_mutation_rmsd(wt_struct, mut_struct, mutation: str) -> float:
    """
    FIX: Perform structural superposition before computing RMSD
    FIX: Use deep copy to avoid mutating input structures
    """
    chain_id = mutation[0]
    resnum = int(mutation[1:-1])

    # FIX: Work with copies to preserve original structures
    wt_model = copy.deepcopy(next(wt_struct.get_models()))
    mut_model = copy.deepcopy(next(mut_struct.get_models()))

    # First, superpose the structures based on backbone atoms
    wt_bb_atoms = []
    mut_bb_atoms = []

    # Collect backbone atoms from both structures for superposition
    for chain in wt_model:
        if chain.id not in mut_model:
            continue
        mut_chain = mut_model[chain.id]

        for res in chain:
            if not is_aa(res):
                continue
            res_id = res.id
            if res_id not in mut_chain:
                continue
            mut_res = mut_chain[res_id]

            # Use backbone atoms for alignment
            for atom_name in ("N", "CA", "C", "O"):
                if atom_name in res and atom_name in mut_res:
                    wt_bb_atoms.append(res[atom_name])
                    mut_bb_atoms.append(mut_res[atom_name])

    # FIX: Superpose structures before computing RMSD
    if wt_bb_atoms:
        sup = Superimposer()
        sup.set_atoms(wt_bb_atoms, mut_bb_atoms)
        sup.apply(list(mut_model.get_atoms()))

    # Now compute RMSD for the mutated residue
    try:
        res1 = wt_model[chain_id][resnum]
        res2 = mut_model[chain_id][resnum]
    except KeyError:
        raise ValueError(
            f"Residue {chain_id}{resnum} not found in one of structures"
        )

    # FIX: Compare sidechain atoms after superposition
    bb = {"N", "CA", "C", "O"}
    atoms1 = [a for a in res1 if a.get_id() not in bb]
    atoms2 = [a for a in res2 if a.get_id() not in bb and
              a.get_id() in {b.get_id() for b in res1}]

    # Match atoms by name
    atom_pairs = []
    for a1 in atoms1:
        for a2 in atoms2:
            if a1.get_id() == a2.get_id():
                atom_pairs.append((a1, a2))
                break

    if not atom_pairs:
        return 0.0

    # Compute RMSD
    diffs2 = []
    for a1, a2 in atom_pairs:
        d = a2.get_coord() - a1.get_coord()
        diffs2.append(np.dot(d, d))

    rmsd = float(np.sqrt(sum(diffs2) / len(diffs2)))
    return rmsd


def compute_center_of_mass_difference(wt_struct, mut_struct) -> float:
    """
    FIX: Now uses mass-weighted COM from corrected compute_center_of_mass()
    """
    com1 = compute_center_of_mass(wt_struct)
    com2 = compute_center_of_mass(mut_struct)
    return float(np.linalg.norm(com1 - com2))
