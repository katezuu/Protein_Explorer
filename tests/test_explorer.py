from explorer import get_phi_psi
from mutation import model_mutation
from metrics import compare_structures, compute_mutation_rmsd
from plotting import plot_ca_scatter, plot_ramachandran
from io_utils import parse_structure
import os
import sys
import pytest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

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

PDB_CONTENT_B = """\
ATOM      1  N   ALA B   1       0.000   0.000   0.000  1.00  0.00           N
ATOM      2  CA  ALA B   1       0.000   0.000   0.000  1.00  0.00           C
TER
END
"""


def write_pdb(content, dirpath, name):
    path = os.path.join(dirpath, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def test_compare_structures_rmsd(tmp_path):
    path1 = write_pdb(PDB_CONTENT1, tmp_path, 'p1.pdb')
    path2 = write_pdb(PDB_CONTENT2, tmp_path, 'p2.pdb')
    rmsd = compare_structures(path1, path2, str(tmp_path))
    assert pytest.approx(rmsd, abs=1e-6) == 0.0
    assert (tmp_path / 'RMSD_p1_p2.txt').exists()


def test_compare_structures_no_common(tmp_path):
    path1 = write_pdb(PDB_CONTENT1, tmp_path, 'p1.pdb')
    path2 = write_pdb(PDB_CONTENT_B, tmp_path, 'p3.pdb')
    rmsd = compare_structures(path1, path2, str(tmp_path))
    assert rmsd == 0.0


def test_plot_and_mutation(tmp_path):
    path = write_pdb(PDB_CONTENT1, tmp_path, 'p.pdb')
    struct = parse_structure(path)
    angles = get_phi_psi(struct)
    scatter_png = tmp_path / 'scatter.png'
    rama_png = tmp_path / 'rama.png'
    plot_ca_scatter(struct, str(scatter_png))
    plot_ramachandran(angles, str(rama_png))
    assert scatter_png.exists() and scatter_png.stat().st_size > 0
    assert rama_png.exists() and rama_png.stat().st_size > 0

    mut_struct = model_mutation(path, 'A1C')
    rmsd = compute_mutation_rmsd(struct, mut_struct, 'A1C')
    assert isinstance(rmsd, float)


def test_fetch_uniprot_variants(monkeypatch):
    class FakeResp:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            pass

    def fake_get(url, timeout=10):
        return FakeResp({'features': [{'type': 'VARIANT', 'location': {
            'start': 1}, 'description': 'mut'}]})

    monkeypatch.setattr('requests.get', fake_get)
    variants = fetch_uniprot_variants('P01234')
    assert variants and variants[0]['position'] == 1
