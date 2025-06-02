import os
import pytest
import sys

# Add the project root to sys.path so that app.py and explorer.py can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Import Flask app for testing


@pytest.fixture
def client():
    """
    Return a Flask test client, with TESTING config enabled.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_get(client):
    """
    GET request to "/" should return status 200 and contain the PDB ID field.
    """
    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "PDB ID #1" in html


def test_post_invalid_pdb(client):
    """
    POST to "/" with an invalid PDB ID (e.g., length != 4) should flash an error.
    """
    response = client.post("/", data={"pdb_id1": "ABC", "pdb_id2": ""}, follow_redirects=True)
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Please enter a valid 4-character PDB ID #1" in html


def test_post_valid_but_nonexistent_pdb(monkeypatch, client):
    """
    POST to "/" with a valid-length PDB ID that does not exist should flash a download error.
    We monkeypatch explorer.download_pdb to force an error.
    """
    import explorer

    def fake_download(pdb_id, out_dir):
        raise FileNotFoundError("PDB not found")

    monkeypatch.setattr(explorer, "download_pdb", fake_download)

    response = client.post("/", data={"pdb_id1": "ZZZZ", "pdb_id2": ""}, follow_redirects=True)
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Failed to download PDB ZZZZ" in html
