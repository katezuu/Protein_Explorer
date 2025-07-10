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
    get_ca_coordinates,
    get_phi_psi,
    plot_ca_scatter,
    plot_ramachandran,
    compare_structures,
    fetch_uniprot_variants,
    fetch_clinvar_variants,
    model_mutation,
    compute_mutation_rmsd,
    compute_center_of_mass_difference,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "replace-this-with-a-secure-key")

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
    GET: render form to input one or two PDB IDs.
    POST: validate input, download and analyze structures, return results.
    """
    if request.method == "POST":
        # Get IDs from form fields
        pdb1 = request.form.get("pdb_id1", "").strip().upper()
        pdb2 = request.form.get("pdb_id2", "").strip().upper()

        # Validate first PDB ID
        if not pdb1 or not validate_pdb_id(pdb1):
            flash("Please enter a valid 4-character PDB ID #1.", "error")
            return redirect(url_for("index"))

        # Validate second PDB ID (optional)
        if pdb2 and not validate_pdb_id(pdb2):
            flash("Please enter a valid 4-character PDB ID #2 or leave blank.", "error")
            return redirect(url_for("index"))

        # Process first structure
        dir1 = os.path.join(OUTPUT_DIR, pdb1)
        os.makedirs(dir1, exist_ok=True)
        try:
            path1 = download_pdb(pdb1, out_dir=dir1)
        except Exception as e:
            flash(f"Failed to download PDB {pdb1}: {e}", "error")
            return redirect(url_for("index"))

        struct1 = parse_structure(path1)
        total1, chains1 = count_residues(struct1)
        seqs1 = get_chain_sequences(struct1)
        center1 = compute_center_of_mass(struct1)
        ca1_path = os.path.join(dir1, f"{pdb1}_ca_scatter.png")
        plot_ca_scatter(struct1, ca1_path)
        angles1 = get_phi_psi(struct1)
        rama1_path = os.path.join(dir1, f"{pdb1}_ramachandran.png")
        plot_ramachandran(angles1, rama1_path)
        ca_coords1 = get_ca_coordinates(struct1)

        result_data = {
            "pdb1": pdb1,
            "total1": total1,
            "chains1": chains1,
            "seqs1": seqs1,
            "center1": center1,
            "ca1_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}_ca_scatter.png"),
            "rama1_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}_ramachandran.png"),
            "pdb1_file_url": url_for("serve_file", pdb_id=pdb1, filename=f"{pdb1}.pdb"),
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
            ca_coords2 = get_ca_coordinates(struct2)

            rmsd_value = compare_structures(path1, path2, OUTPUT_DIR)
            result_data.update({
                "pdb2": pdb2,
                "total2": total2,
                "chains2": chains2,
                "seqs2": seqs2,
                "center2": center2,
                "ca2_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}_ca_scatter.png"),
                "rama2_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}_ramachandran.png"),
                "pdb2_file_url": url_for("serve_file", pdb_id=pdb2, filename=f"{pdb2}.pdb"),
                "angles2": angles2,
                "ca_coords2": ca_coords2,
                "rmsd": rmsd_value,
            })

        return render_template("result.html", **result_data)

    # GET request: render form
    return render_template("index.html")

@app.route("/mutations", methods=["GET"])
def mutations_form():
    return render_template("mutations.html")

@app.route("/analyze_mutation", methods=["POST"])
def analyze_mutation():
    pdb_id = request.form.get("pdb_id", "").strip().upper()
    mutation = request.form.get("mutation", "").strip()

    if not pdb_id or not validate_pdb_id(pdb_id):
        flash("Please enter a valid 4-character PDB ID.", "error")
        return redirect(url_for("mutations_form"))
    if not mutation:
        flash("Please provide a mutation (e.g., A123C).", "error")
        return redirect(url_for("mutations_form"))

    dir1 = os.path.join(OUTPUT_DIR, f"{pdb_id}_mut")
    os.makedirs(dir1, exist_ok=True)
    try:
        pdb_path = download_pdb(pdb_id, out_dir=dir1)
    except Exception as e:
        flash(f"Failed to download PDB {pdb_id}: {e}", "error")
        return redirect(url_for("mutations_form"))

    wt_struct = parse_structure(pdb_path)
    mut_struct = model_mutation(pdb_path, mutation)
    from Bio.PDB import PDBIO
    io = PDBIO()
    io.set_structure(mut_struct)
    io.save(os.path.join(dir1, f"{pdb_id}_mut.pdb"))

    rmsd_val = compute_mutation_rmsd(wt_struct, mut_struct)
    com_diff = compute_center_of_mass_difference(wt_struct, mut_struct)

    uniprot_variants = []
    clinvar_variants = []
    try:
        uniprot_variants = fetch_uniprot_variants(pdb_id)
    except Exception:
        pass
    try:
        clinvar_variants = fetch_clinvar_variants(pdb_id)
    except Exception:
        pass

    return render_template(
        "mutation_result.html",
        pdb_id=pdb_id,
        mutation=mutation,
        rmsd=rmsd_val,
        com_diff=com_diff,
        uniprot_variants=uniprot_variants,
        clinvar_variants=clinvar_variants,
    )

@app.route("/outputs/<pdb_id>/<filename>")
def serve_file(pdb_id, filename):
    return send_from_directory(os.path.join(OUTPUT_DIR, pdb_id), filename)

@app.route("/api/metrics/<pdb_id>")
def api_metrics(pdb_id):
    if not validate_pdb_id(pdb_id):
        return {"error": "invalid pdb id"}, 400
    try:
        pdb_path = download_pdb(pdb_id, out_dir=OUTPUT_DIR)
    except Exception as e:
        return {"error": str(e)}, 500
    struct = parse_structure(pdb_path)
    total, chains = count_residues(struct)
    center = compute_center_of_mass(struct).tolist()
    return {"pdb_id": pdb_id, "total_residues": total, "chains": chains, "center_of_mass": center}

@app.route("/api/mutation_metrics/<pdb_id>/<mutation>")
def api_mutation_metrics(pdb_id, mutation):
    if not validate_pdb_id(pdb_id):
        return {"error": "invalid pdb id"}, 400

    try:
        pdb_path   = download_pdb(pdb_id, out_dir=OUTPUT_DIR)
        wt_struct  = parse_structure(pdb_path)
        mut_struct = model_mutation(pdb_path, mutation)
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
