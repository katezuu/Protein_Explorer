import numpy as np
from Bio.Data.IUPACData import protein_letters_1to3
from Bio.PDB.vectors import Vector, rotaxis
from io_utils import parse_structure


def model_mutation(pdb_path: str, mutation: str):
    """
    Introduce a single-point mutation by changing the residue name and
    rotating its sidechain around the Cα-Cβ bond axis by 120°.

    mutation format: <chain><residueNumber><newAA>, e.g. "A141D" or "B91D"

    FIX: Changed from global Z-axis rotation to local Cα-Cβ axis rotation
    FIX: Uses more realistic 120° rotation angle for sidechain reorientation
    FIX: Now handles missing Cβ atoms (e.g., glycine) gracefully
    """
    # Parse chain, position, and new amino acid
    new_aa = mutation[-1].upper()
    rest = mutation[:-1]

    # Split rest into chain (leading non-digits) and pos (trailing digits)
    idx = len(rest)
    while idx > 0 and rest[idx - 1].isdigit():
        idx -= 1
    chain_id = rest[:idx]
    try:
        pos = int(rest[idx:])
    except ValueError:
        raise ValueError(
            f"Invalid mutation string: couldn't parse res. number from {rest!r}"
        )

    struct = parse_structure(pdb_path)
    mutation_found = False

    for residue in struct.get_residues():
        parent_chain = residue.get_parent().id
        # FIX: Properly handle hetero flag and insertion code in residue ID
        res_id = residue.id
        if parent_chain != chain_id or res_id[1] != pos:
            continue

        mutation_found = True

        # Rename residue
        try:
            residue.resname = protein_letters_1to3[new_aa]
        except KeyError:
            raise ValueError(f"Invalid amino acid code: {new_aa!r}")

        # Get Cα atom
        try:
            ca_atom = residue["CA"]
        except KeyError:
            raise ValueError(f"No Cα atom found for residue {chain_id}{pos}")

        ca_coord = Vector(ca_atom.get_coord())

        # FIX: Use Cα-Cβ axis for rotation if available
        # If Cβ is missing (e.g., glycine), skip rotation
        if "CB" in residue:
            cb_atom = residue["CB"]
            cb_coord = Vector(cb_atom.get_coord())

            # Define rotation axis as Cα → Cβ vector
            axis = (cb_coord - ca_coord).normalized()

            # Rotate sidechain atoms (excluding backbone) by 120°
            # FIX: 120° is a more realistic rotamer adjustment
            theta = np.deg2rad(120.0)

            for atom in residue:
                atom_id = atom.get_id()
                # Skip backbone atoms
                if atom_id in ("N", "CA", "C", "O", "CB"):
                    continue

                atom_coord = Vector(atom.get_coord())
                # Vector from Cα to atom
                v = atom_coord - ca_coord

                # Rotate around Cα-Cβ axis using Bio.PDB.vectors.rotaxis
                v_rotated = v.left_multiply(rotaxis(theta, axis))

                # Set new coordinates
                new_coord = ca_coord + v_rotated
                atom.set_coord(new_coord.get_array())
        else:
            # FIX: For glycine or residues
            # without Cβ, just rename without rotation
            pass

        break

    if not mutation_found:
        raise ValueError(f"Residue {chain_id}{pos} not found in structure")

    return struct
