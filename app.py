#!/usr/bin/env python3
"""
app.py

Flask web application for Protein Structure Explorer:
- Downloads PDB or mmCIF (with gzip) with automatic fallback.
- Parses structures using correct format (.pdb or .cif).
- Analyzes single structures or pairs (residue counts, center-of-mass, RMSD).
- Serves files and mutation API.
"""

import os
import re
import gzip
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from explorer import (
    download_pdb,
    download_cif,
    parse_structure,
    count_residues,
    get_chain_sequences,
    compute_center_of_mass,
    get_ca_coordinates,
    get_phi_psi,
    plot_ca_scatter,
    plot_ramachandran,
    compare_structures,
    model_mutation,
    compute_mutation_rmsd,
    compute_center_of_mass_difference,
    fetch_uniprot_variants,
    fetch_clinvar_variants,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "replace-this-with-a-secure-key")

BASE_DIR   = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDB_PATTERN = re.compile(r"^[0-9A-Za-z]{4}$")

def validate_pdb_id(pdb_id: str) -> bool:
    return bool(PDB_PATTERN.match(pdb_id))

def download_structure(pdb_id: str, out_dir: str):
    """
    Try mmCIF (and gzip it), fall back to PDB.
    Returns (serve_filename, fmt, parse_filename) where:
      - serve_filename: what to serve to client (e.g. '1AKE.cif.gz' or '1AKE.pdb')
      - fmt: 'mmcif_gz', 'mmcif', or 'pdb'
      - parse_filename: the uncompressed file to hand to parse_structure
    """
    pdb_id = pdb_id.upper()
    # try CIF
    try:
        cif_path = download_cif(pdb_id, out_dir)
        cif_name = os.path.basename(cif_path)
        gz_path  = cif_path + ".gz"
        gz_name  = cif_name + ".gz"
        if not os.path.exists(gz_path):
            with open(cif_path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                f_out.writelines(f_in)
        return gz_name, "mmcif_gz", cif_name
    except Exception:
        # fallback to PDB
        pdb_path = download_pdb(pdb_id, out_dir)
        pdb_name = os.path.basename(pdb_path)
        return pdb_name, "pdb", pdb_name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdb1 = request.form.get("pdb_id1", "").strip().upper()
        pdb2 = request.form.get("pdb_id2", "").strip().upper()

        if not pdb1 or not validate_pdb_id(pdb1):
            flash("Please enter a valid 4-character PDB ID #1.", "error")
            return redirect(url_for("index"))
        if pdb2 and not validate_pdb_id(pdb2):
            flash("Please enter a valid 4-character PDB ID #2 or leave blank.", "error")
            return redirect(url_for("index"))

        # Process first structure
        dir1 = os.path.join(OUTPUT_DIR, pdb1)
        os.makedirs(dir1, exist_ok=True)
        try:
            serve1, fmt1, parse1 = download_structure(pdb1, dir1)
        except Exception as e:
            flash(f"Failed to download PDB {pdb1}: {e}", "error")
            return redirect(url_for("index"))
        path1 = os.path.join(dir1, parse1)

        struct1, total1, chains1, seqs1, center1, angles1, ca_coords1 = (
            parse_structure(path1),
            *count_residues(parse_structure(path1)),
            get_chain_sequences(parse_structure(path1)),
            compute_center_of_mass(parse_structure(path1)),
            get_phi_psi(parse_structure(path1)),
            get_ca_coordinates(parse_structure(path1)),
        )
        ca1_png = os.path.join(dir1, f"{pdb1}_ca_scatter.png")
        plot_ca_scatter(struct1, ca1_png)
        rama1_png = os.path.join(dir1, f"{pdb1}_ramachandran.png")
        plot_ramachandran(angles1, rama1_png)

        result_data = {
            "pdb1": pdb1,
            "serve1": serve1,
            "fmt1": fmt1,
            "url1": url_for("serve_file", pdb_id=pdb1, filename=serve1),
            "total1": total1,
            "chains1": chains1,
            "seqs1": seqs1,
            "center1": center1,
            "ca1_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}_ca_scatter.png"),
            "rama1_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}_ramachandran.png"),
            "angles1": angles1,
            "ca_coords1": ca_coords1,
            "rmsd": None,
            "pdb2": None,
        }

        # Process second structure if provided
        if pdb2:
            dir2 = os.path.join(OUTPUT_DIR, pdb2)
            os.makedirs(dir2, exist_ok=True)
            try:
                serve2, fmt2, parse2 = download_structure(pdb2, dir2)
            except Exception as e:
                flash(f"Failed to download PDB {pdb2}: {e}", "error")
                return redirect(url_for("index"))
            path2 = os.path.join(dir2, parse2)

            struct2, total2, chains2, seqs2, center2, angles2, ca_coords2 = (
                parse_structure(path2),
                *count_residues(parse_structure(path2)),
                get_chain_sequences(parse_structure(path2)),
                compute_center_of_mass(parse_structure(path2)),
                get_phi_psi(parse_structure(path2)),
                get_ca_coordinates(parse_structure(path2)),
            )
            ca2_png = os.path.join(dir2, f"{pdb2}_ca_scatter.png")
            plot_ca_scatter(struct2, ca2_png)
            rama2_png = os.path.join(dir2, f"{pdb2}_ramachandran.png")
            plot_ramachandran(angles2, rama2_png)
            rmsd_value = compare_structures(path1, path2, OUTPUT_DIR)

            result_data.update({
                "pdb2": pdb2,
                "serve2": serve2,
                "fmt2": fmt2,
                "url2": url_for("serve_file", pdb_id=pdb2, filename=serve2),
                "total2": total2,
                "chains2": chains2,
                "seqs2": seqs2,
                "center2": center2,
                "ca2_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}_ca_scatter.png"),
                "rama2_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}_ramachandran.png"),
                "angles2": angles2,
                "ca_coords2": ca_coords2,
                "rmsd": rmsd_value,
            })

        return render_template("result.html", **result_data)

    return render_template("index.html")

@app.route("/outputs/<pdb_id>/<filename>")
def serve_file(pdb_id, filename):
    return send_from_directory(os.path.join(OUTPUT_DIR, pdb_id), filename)

@app.route("/api/metrics/<pdb_id>")
def api_metrics(pdb_id):
    if not validate_pdb_id(pdb_id):
        return {"error": "invalid pdb id"}, 400
    try:
        serve, fmt, parse = download_structure(pdb_id, out_dir=OUTPUT_DIR)
        path = os.path.join(OUTPUT_DIR, pdb_id, parse)
        struct = parse_structure(path)
        total, chains = count_residues(struct)
        center = compute_center_of_mass(struct).tolist()
        return {
            "pdb_id": pdb_id,
            "total_residues": total,
            "chains": chains,
            "center_of_mass": center,
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/api/mutation_metrics/<pdb_id>/<mutation>")
def api_mutation_metrics(pdb_id, mutation):
    if not validate_pdb_id(pdb_id):
        return {"error": "invalid pdb id"}, 400
    try:
        serve, fmt, parse = download_structure(pdb_id, out_dir=OUTPUT_DIR)
        path = os.path.join(OUTPUT_DIR, pdb_id, parse)
        wt_struct  = parse_structure(path)
        mut_struct = model_mutation(path, mutation)
        rmsd_val   = compute_mutation_rmsd(wt_struct, mut_struct)
        com_diff   = compute_center_of_mass_difference(wt_struct, mut_struct)
        return {
            "pdb_id": pdb_id,
            "mutation": mutation,
            "rmsd": rmsd_val,
            "center_of_mass_diff": com_diff,
        }
    except Exception as e:
        app.logger.exception("Mutation analysis failed")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
