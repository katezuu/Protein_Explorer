import pytest
from app import create_app
import io_utils


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_get(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "PDB ID #1" in resp.get_data(as_text=True)


def test_post_invalid_pdb(client):
    resp = client.post(
        "/",
        data={"pdb_id1": "ABC", "pdb_id2": ""},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert (
            "Please enter a valid 4-character PDB ID #1"
            in resp.get_data(as_text=True)
    )


def test_post_valid_but_nonexistent_pdb(monkeypatch, client):
    def fake_download():
        raise FileNotFoundError("PDB not found")

    monkeypatch.setattr(io_utils, "download_pdb", fake_download)

    resp = client.post(
        "/",
        data={"pdb_id1": "ZZZZ", "pdb_id2": ""},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "Failed to download PDB ZZZZ" in resp.get_data(as_text=True)
