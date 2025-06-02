import os
import numpy as np
import pytest
import sys

# Add the project root to sys.path so that explorer.py can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from explorer import (
    compare_structures,
    plot_ramachandran,
    plot_ca_scatter,
    get_phi_psi,
    parse_structure,
)

# Two minimal PDB contents with two Cα atoms each:
# 1) First PDB: Cα at (0,0,0) and (1,0,0)
# 2) Second PDB: Cα at (0,0,0) and (2,0,0)
#
# After superimposition, Superimposer aligns them perfectly, resulting in RMSD = 0.0.

PDB_CONTENT1 = """\
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N  
ATOM      2  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C  
ATOM      3  C   ALA A   1       1.000   0.000   0.000  1.00  0.00           C  
ATOM      4  O   ALA A   1       2.000   0.000   0.000  1.00  0.00           O  
TER
END
"""

PDB_CONTENT2 = """\
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N  
ATOM      2  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C  
ATOM      3  C   ALA A   1       2.000   0.000   0.000  1.00  0.00           C  
ATOM      4  O   ALA A   1       3.000   0.000   0.000  1.00  0.00           O  
TER
END
"""

def write_temp_pdb(content, dirpath, filename):
    """
    Helper: write the given content to a PDB file under dirpath.
    Returns the full path to the newly written file.
    """
    path = os.path.join(dirpath, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_compare_structures_rmsd(tmp_path):
    """
    Test compare_structures on two PDBs with two residues each.
    After alignment, RMSD should be 0.0.
    """
    dir1 = tmp_path / "p1"
    dir2 = tmp_path / "p2"
    dir1.mkdir()
    dir2.mkdir()

    path1 = write_temp_pdb(PDB_CONTENT1, str(dir1), "P1.pdb")
    path2 = write_temp_pdb(PDB_CONTENT2, str(dir2), "P2.pdb")

    rmsd = compare_structures(path1, path2, str(tmp_path))

    # Check that the RMSD text file was created
    expected_txt = tmp_path / "RMSD_P1_P2.txt"
    assert expected_txt.exists()

    # After superimposition, RMSD ought to be exactly 0.0
    assert pytest.approx(rmsd, abs=1e-6) == 0.0


def test_plot_functions(tmp_path):
    """
    Verify that plot_ca_scatter and plot_ramachandran create non-empty PNG files,
    and that get_phi_psi returns a list of (phi, psi) tuples.
    """
    # Create a temporary directory and PDB file
    dirp = tmp_path / "pdb"
    dirp.mkdir()
    path = write_temp_pdb(PDB_CONTENT1, str(dirp), "P1.pdb")

    struct = parse_structure(path)
    angles = get_phi_psi(struct)
    assert isinstance(angles, list)

    scatter_png = tmp_path / "scatter.png"
    rama_png = tmp_path / "rama.png"

    plot_ca_scatter(struct, str(scatter_png))
    plot_ramachandran(angles, str(rama_png))

    assert scatter_png.exists() and scatter_png.stat().st_size > 0
    assert rama_png.exists() and rama_png.stat().st_size > 0
