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
    Ищет в структуре цепь, в которой есть аминокислотный
    остаток с данным номером.
    Возвращает ID цепи (строку), либо None, если не найден.
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

    # 1) Скачиваем и разбираем WT-структуру
    serve_name, fmt = download_structure(
        PDB_ID,
        os.path.join(OUTPUT_ROOT, PDB_ID)
    )
    if fmt == "mmcif_gz":
        # serve_name == "1AKE.cif.gz" → parse_name == "1AKE.cif"
        parse_name = serve_name[:-3]
    else:
        # serve_name == "1AKE.cif" или "1AKE.pdb"
        parse_name = serve_name
    wt_path = os.path.join(OUTPUT_ROOT, PDB_ID, parse_name)
    wt_struct = parse_structure(wt_path)

    # 2) Открываем CSV с мутациями и создаём выходной CSV
    input_csv = "mutations_1AKE.csv"
    output_csv = "mutation_results.csv"
    with open(input_csv, newline="") as f_in, \
            open(
                output_csv,
                "w",
                newline=""
            ) as f_out:

        reader = csv.DictReader(f_in)
        # добавляем новые колонки
        fieldnames = (
                reader.fieldnames
                + ["chain", "mutation", "rmsd", "com_shift"]
        )
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            pos = int(row["residue_number"])
            mut = row["mutated"]

            # 3) Определяем цепь
            chain = row.get("chain")
            if not chain:
                chain = find_chain_for_residue(wt_struct, pos)
            if chain is None:
                print(
                    f"[WARNING] Residue {pos} not found in any chain "
                    "→ skipped"
                )
                continue

            # 4) Формируем строку мутации и считаем метрики
            mut_str = f"{chain}{pos}{mut}"
            try:
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
            except Exception as e:
                print(f"[WARNING] Error for {mut_str}: {e}")
                rmsd, com_shift = "", ""

            # 5) Записываем в CSV
            row.update(
                {
                    "chain": chain,
                    "mutation": mut_str,
                    "rmsd": rmsd,
                    "com_shift": com_shift
                }
            )
            writer.writerow(row)

    print(f"Done! Results saved to {output_csv}")


if __name__ == "__main__":
    main()
