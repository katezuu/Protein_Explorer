import os
import numpy as np
from Bio.PDB import Superimposer, is_aa

from io_utils import parse_structure


def compute_center_of_mass(structure) -> np.ndarray:
    coords = [atom.get_coord() for atom in structure.get_atoms()]
    if not coords:
        # если вдруг нет атомов
        return np.array([np.nan, np.nan, np.nan])
    return np.mean(coords, axis=0)


def compare_structures(path1: str, path2: str, out_dir: str) -> float:
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

    if not ca1:
        return 0.0

    sup = Superimposer()
    sup.set_atoms(ca1, ca2)
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
    chain_id = mutation[0]
    resnum = int(mutation[1:-1])

    model1 = next(wt_struct.get_models())
    model2 = next(mut_struct.get_models())

    try:
        res1 = model1[chain_id][resnum]
        res2 = model2[chain_id][resnum]
    except KeyError:
        raise ValueError(
            f"Residue {chain_id}{resnum} not found in one of structures")

    bb = {"N", "CA", "C", "O"}
    atoms1 = [a for a in res1 if a.get_id() not in bb and a.get_id()
              in {b.get_id() for b in res2}]
    atoms2 = [res2[a.get_id()] for a in atoms1]

    if not atoms1:
        return 0.0

    diffs2 = []
    for a1, a2 in zip(atoms1, atoms2):
        d = a2.get_coord() - a1.get_coord()
        diffs2.append(np.dot(d, d))
    rmsd = float(np.sqrt(sum(diffs2) / len(diffs2)))
    return rmsd


def compute_center_of_mass_difference(wt_struct, mut_struct) -> float:
    com1 = compute_center_of_mass(wt_struct)
    com2 = compute_center_of_mass(mut_struct)
    return float(np.linalg.norm(com1 - com2))
