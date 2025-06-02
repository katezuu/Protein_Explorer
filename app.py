#!/usr/bin/env python3
"""
app.py

Flask web application for Protein Structure Explorer:
- Validates user input (4-character PDB IDs).
- Downloads and parses PDB structures.
- Calls explorer.py functions to compute and plot.
- Renders results using Jinja2 templates (Bootstrap 5 styling).
"""

import os
import re
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
from explorer import (
    download_pdb,
    parse_structure,
    count_residues,
    get_chain_sequences,
    compute_center_of_mass,
    get_phi_psi,
    plot_ca_scatter,
    plot_ramachandran,
    compare_structures
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-this-with-a-secure-key"  # Change this to a secure random key in production

# Base directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Regex to validate a 4-character PDB ID (letters and digits)
PDB_PATTERN = re.compile(r"^[0-9A-Za-z]{4}$")


def validate_pdb_id(pdb_id: str) -> bool:
    """Return True if pdb_id matches exactly 4 alphanumeric characters."""
    return bool(PDB_PATTERN.match(pdb_id))


@app.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Render the form for entering one or two PDB IDs.
    POST: Validate input, download and analyze structures, then render results.
    """
    if request.method == "POST":
        pdb1 = request.form.get("pdb_id1", "").strip().upper()
        pdb2 = request.form.get("pdb_id2", "").strip().upper()

        # Validate first PDB ID (required)
        if not pdb1 or not validate_pdb_id(pdb1):
            flash("Please enter a valid 4-character PDB ID #1.", "error")
            return redirect(url_for("index"))

        # Validate second PDB ID if provided
        if pdb2 and not validate_pdb_id(pdb2):
            flash("Please enter a valid 4-character PDB ID #2 or leave blank.", "error")
            return redirect(url_for("index"))

        # Create output folder for the first structure
        dir1 = os.path.join(OUTPUT_DIR, pdb1)
        os.makedirs(dir1, exist_ok=True)

        # Download and parse the first structure
        try:
            path1 = download_pdb(pdb1, out_dir=dir1)
        except Exception as e:
            flash(f"Failed to download PDB {pdb1}: {e}", "error")
            return redirect(url_for("index"))

        struct1 = parse_structure(path1)
        total1, chains1 = count_residues(struct1)
        seqs1 = get_chain_sequences(struct1)
        center1 = compute_center_of_mass(struct1)

        # Generate static plots for the first structure
        ca1_path = os.path.join(dir1, f"{pdb1}_ca_scatter.png")
        plot_ca_scatter(struct1, ca1_path)
        angles1 = get_phi_psi(struct1)
        rama1_path = os.path.join(dir1, f"{pdb1}_ramachandran.png")
        plot_ramachandran(angles1, rama1_path)

        result_data = {
            "pdb1": pdb1,
            "total1": total1,
            "chains1": chains1,
            "seqs1": seqs1,
            "center1": center1,
            "ca1_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}_ca_scatter.png"),
            "rama1_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}_ramachandran.png"),
            "pdb1_file_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}.pdb"),
            "rmsd": None,
            "pdb2": None,
        }

        # If a second PDB ID is provided, analyze it and compute RMSD
        if pdb2:
            dir2 = os.path.join(OUTPUT_DIR, pdb2)
            os.makedirs(dir2, exist_ok=True)
            try:
                path2 = download_pdb(pdb2, out_dir=dir2)
            except Exception as e:
                flash(f"Failed to download PDB {pdb2}: {e}", "error")
                return redirect(url_for("index"))

            struct2 = parse_structure(path2)
            total2, chains2 = count_residues(struct2)
            seqs2 = get_chain_sequences(struct2)
            center2 = compute_center_of_mass(struct2)

            ca2_path = os.path.join(dir2, f"{pdb2}_ca_scatter.png")
            plot_ca_scatter(struct2, ca2_path)
            angles2 = get_phi_psi(struct2)
            rama2_path = os.path.join(dir2, f"{pdb2}_ramachandran.png")
            plot_ramachandran(angles2, rama2_path)

            # Compute RMSD and save under OUTPUT_DIR
            rmsd_value = compare_structures(path1, path2, OUTPUT_DIR)

            result_data.update(
                {
                    "pdb2": pdb2,
                    "total2": total2,
                    "chains2": chains2,
                    "seqs2": seqs2,
                    "center2": center2,
                    "ca2_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}_ca_scatter.png"),
                    "rama2_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}_ramachandran.png"),
                    "pdb2_file_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}.pdb"),
                    "rmsd": rmsd_value,
                }
            )

        return render_template("result.html", **result_data)

    # For GET requests, render the empty form
    return render_template("index.html")


@app.route("/outputs/<pdb_id>/<filename>")
def serve_file(pdb_id, filename):
    """
    Serve static files (PNG, PDB) from outputs/<pdb_id>/ directory.
    """
    return send_from_directory(os.path.join(OUTPUT_DIR, pdb_id), filename)


if __name__ == "__main__":
    app.run(debug=True)
