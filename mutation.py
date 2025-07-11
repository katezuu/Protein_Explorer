import numpy as np
from Bio.Data.IUPACData import protein_letters_1to3

from io_utils import parse_structure


def model_mutation(pdb_path: str, mutation: str):
    struct = parse_structure(pdb_path)
    new_aa = mutation[-1].upper()
    pos = int(mutation[1:-1])

    theta = np.deg2rad(45.0)
    axis = np.array([0.0, 0.0, 1.0])
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)

    for residue in struct.get_residues():
        if residue.id[1] != pos:
            continue
        try:
            residue.resname = protein_letters_1to3[new_aa]
        except KeyError:
            raise ValueError(f"Invalid amino-acid code: {new_aa}")
        ca = residue["CA"]
        ca_coord = ca.get_coord()
        for atom in residue:
            if atom.get_id() == "CA":
                continue
            v = atom.get_coord() - ca_coord
            atom.set_coord(ca_coord + R.dot(v))
        break

    return struct
