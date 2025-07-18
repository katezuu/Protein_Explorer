import numpy as np
from Bio.Data.IUPACData import protein_letters_1to3

from io_utils import parse_structure


def model_mutation(pdb_path: str, mutation: str):
    """
    Introduce a single‐point mutation by changing the residue name and
    rotating its sidechain by 45° around the Cα.

    mutation format: <chain><residueNumber><newAA>, e.g. "DB91D" or "A141D"
    """
    # parse chain, position, and new amino‐acid
    new_aa = mutation[-1].upper()
    rest = mutation[:-1]
    # split rest into chain (leading non-digits) and pos (trailing digits)
    idx = len(rest)
    while idx > 0 and rest[idx - 1].isdigit():
        idx -= 1
    chain_id = rest[:idx]
    try:
        pos = int(rest[idx:])
    except ValueError:
        raise ValueError(f"Invalid mutation string: could not parse residue number from {rest!r}")

    # rotation matrix (Rodrigues' formula) for 45° about Z
    theta = np.deg2rad(45.0)
    axis = np.array([0.0, 0.0, 1.0])
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)

    struct = parse_structure(pdb_path)

    for residue in struct.get_residues():
        parent_chain = residue.get_parent().id
        if parent_chain != chain_id or residue.id[1] != pos:
            continue

        # rename
        try:
            residue.resname = protein_letters_1to3[new_aa]
        except KeyError:
            raise ValueError(f"Invalid amino‐acid code: {new_aa!r}")

        # now grab Cα (or fail with a meaningful message)
        try:
            ca_atom = residue["CA"]
        except KeyError:
            raise ValueError(f"No Cα atom found for residue {chain_id}{pos}")

        ca_coord = ca_atom.get_coord()
        for atom in residue:
            if atom.get_id() == "CA":
                continue
            v = atom.get_coord() - ca_coord
            atom.set_coord(ca_coord + R.dot(v))
        break
    else:
        raise ValueError(f"Residue {chain_id}{pos} not found in structure")

    return struct
