import os
import csv
import pandas as pd

from explorer import download_structure, parse_structure, model_mutation
from metrics import compute_mutation_rmsd, compute_center_of_mass_difference

#  ————————————————————————————————————————————————————————————————
# Параметры
PDB_ID = "1AKE"
MUT_CSV = "mutations_1AKE.csv"
OUTPUT_ROOT = "outputs"
RESULTS_DIR = "results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "mutation_metrics_1AKE.csv")
#  ————————————————————————————————————————————————————————————————

os.makedirs(RESULTS_DIR, exist_ok=True)

# 1) Скачиваем нужную структуру (mmCIF.gz или PDB)
serve_name, fmt, parse_name = download_structure(
    PDB_ID,
    os.path.join(OUTPUT_ROOT, PDB_ID)
)
wt_path = os.path.join(OUTPUT_ROOT, PDB_ID, parse_name)

# 2) Парсим «дикую» структуру
wt_struct = parse_structure(wt_path)

# 3) Читаем CSV со списком мутаций
with open(MUT_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    muts = list(reader)

# 4) Для каждой мутации делаем модель, считаем RMSD и COM-сдвиг
results = []
for m in muts:
    # собираем строку вида A141D
    mut_str = f"{m['original']}{m['residue_number']}{m['mutated']}"
    try:
        mut_struct = model_mutation(wt_path, mut_str)
        rmsd = compute_mutation_rmsd(wt_struct, mut_struct)
        com = compute_center_of_mass_difference(wt_struct, mut_struct)
    except Exception as e:
        rmsd, com = None, None
    results.append({
        **m,
        "mutation": mut_str,
        "rmsd": rmsd,
        "com_shift": com
    })

# 5) Сохраняем таблицу результатов
df = pd.DataFrame(results)
df.to_csv(RESULTS_FILE, index=False)
print(f"Done: {len(results)} records → {RESULTS_FILE}")
