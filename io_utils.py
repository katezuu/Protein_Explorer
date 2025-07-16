import os
import gzip
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from Bio.PDB import PDBParser, MMCIFParser
from typing import Union
from config import CACHE_DIR


def _get_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def download_cif(pdb_id: str, out_dir: str) -> str:
    pdb_id = pdb_id.upper()
    cache_cif = os.path.join(CACHE_DIR, f"{pdb_id}.cif")
    cache_gz = cache_cif + ".gz"
    if os.path.exists(cache_cif) and os.path.exists(cache_gz):
        return cache_cif

    session = _get_session()
    url = f"https://files.rcsb.org/download/{pdb_id}.cif"
    resp = session.get(url, timeout=30)
    resp.raise_for_status()

    os.makedirs(out_dir, exist_ok=True)
    out_cif = os.path.join(out_dir, f"{pdb_id}.cif")
    with open(out_cif, "wb") as f:
        f.write(resp.content)
    with open(cache_cif, "wb") as f:
        f.write(resp.content)
    with gzip.open(cache_gz, "wb") as gz:
        gz.write(resp.content)
    return out_cif


def download_pdb(pdb_id: str, out_dir: str) -> str:
    pdb_id = pdb_id.upper()
    cache_pdb = os.path.join(CACHE_DIR, f"{pdb_id}.pdb")
    if os.path.exists(cache_pdb):
        return cache_pdb

    session = _get_session()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    resp = session.get(url, timeout=30)
    resp.raise_for_status()

    os.makedirs(out_dir, exist_ok=True)
    out_pdb = os.path.join(out_dir, f"{pdb_id}.pdb")
    with open(out_pdb, "wb") as f:
        f.write(resp.content)
    with open(cache_pdb, "wb") as f:
        f.write(resp.content)
    return out_pdb


def download_structure(pdb_id: str, out_dir: str):
    try:
        cif_path = download_cif(pdb_id, out_dir)
        gz_path = cif_path + ".gz"
        if os.path.exists(gz_path):
            return os.path.basename(gz_path), "mmcif_gz"
        return os.path.basename(cif_path), "mmcif"
    except Exception:
        pdb_path = download_pdb(pdb_id, out_dir)
        return os.path.basename(pdb_path), "pdb"


def parse_structure(path: str):
    ext = os.path.splitext(path)[1].lower()
    parser: Union[PDBParser, MMCIFParser]
    if ext == ".pdb":
        parser = PDBParser(QUIET=True)
    elif ext in (".cif", ".mmcif"):
        parser = MMCIFParser(QUIET=True)
    else:
        raise ValueError(f"Unsupported format: {ext}")
    return parser.get_structure(os.path.basename(path), path)
