import os
import csv
from io_utils import download_structure, parse_structure
from mutation import model_mutation
from metrics import (
    compute_mutation_rmsd,
    compute_center_of_mass_difference
)
from Bio.PDB import is_aa


def find_chain_for_residue(structure, residue_number):
    """
    Search structure for a chain containing an amino acid residue
    with the given number.
    Returns chain ID (string), or None if not found.
    """
    for model in structure:
        for chain in model:
            for res in chain:
                if is_aa(res) and res.id[1] == residue_number:
                    return chain.id
    return None


def main():
    PDB_ID = "1AKE"
    OUTPUT_ROOT = "outputs"
    os.makedirs(os.path.join(OUTPUT_ROOT, PDB_ID), exist_ok=True)

    # 1) Download and parse WT structure
    serve_name, fmt = download_structure(
        PDB_ID,
        os.path.join(OUTPUT_ROOT, PDB_ID)
    )
    if fmt == "mmcif_gz":
        # serve_name == "1AKE.cif.gz" → parse_name == "1AKE.cif"
        parse_name = serve_name[:-3]
    else:
        # serve_name == "1AKE.cif" or "1AKE.pdb"
        parse_name = serve_name
    wt_path = os.path.join(OUTPUT_ROOT, PDB_ID, parse_name)

    # 2) Open input CSV and create output CSV
    input_csv = "mutations_1AKE.csv"
    output_csv = "mutation_results.csv"

    # FIX: Added counters for success/failure tracking
    success_count = 0
    failure_count = 0

    with open(input_csv, newline="") as f_in, \
            open(output_csv, "w", newline="") as f_out:

        reader = csv.DictReader(f_in)
        # Add new columns
        fieldnames = (
                list(reader.fieldnames)
                + ["chain", "mutation", "rmsd", "com_shift", "status"]
        )
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            pos = int(row["residue_number"])
            mut = row["mutated"]

            # FIX: Parse WT structure fresh
            # for each mutation to avoid coordinate drift
            wt_struct = parse_structure(wt_path)

            # 3) Determine chain
            chain = row.get("chain")
            if not chain:
                chain = find_chain_for_residue(wt_struct, pos)
            if chain is None:
                print(
                    f"[WARNING] Residue {pos} not found in any chain → skipped"
                )
                row.update({
                    "chain": "",
                    "mutation": "",
                    "rmsd": "",
                    "com_shift": "",
                    "status": "residue_not_found"
                })
                writer.writerow(row)
                failure_count += 1
                continue

            # 4) Build mutation string and compute metrics
            mut_str = f"{chain}{pos}{mut}"
            try:
                # FIX: Each mutation operates on fresh WT structure
                mut_struct = model_mutation(wt_path, mut_str)

                rmsd = compute_mutation_rmsd(
                    wt_struct,
                    mut_struct,
                    mut_str
                )
                com_shift = compute_center_of_mass_difference(
                    wt_struct,
                    mut_struct
                )

                # FIX: Format to reasonable precision
                rmsd_str = f"{rmsd:.4f}"
                com_shift_str = f"{com_shift:.4f}"
                status = "success"
                success_count += 1

            except Exception as e:
                print(f"[WARNING] Error for {mut_str}: {e}")
                rmsd_str = ""
                com_shift_str = ""
                # Truncate long error messages
                status = f"error: {str(e)[:50]}"
                failure_count += 1

            # 5) Write to CSV
            row.update({
                "chain": chain,
                "mutation": mut_str,
                "rmsd": rmsd_str,
                "com_shift": com_shift_str,
                "status": status
            })
            writer.writerow(row)

    # FIX: Print summary statistics
    print(f"\nDone! Results saved to {output_csv}")
    print(f"Successfully processed: {success_count} mutations")
    print(f"Failed: {failure_count} mutations")
    print(f"Total: {success_count + failure_count} mutations")


if __name__ == "__main__":
    main()
