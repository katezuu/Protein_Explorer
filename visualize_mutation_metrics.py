"""
Визуализация результатов пакетного расчёта мутаций:
 - строит два барплота: RMSD и смещение COM по каждой мутации
"""
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def plot_metrics(df, col, title, ylabel, out_file):
    # сортировка по позиции для стабильного порядка
    df = df.sort_values(["residue_number"], kind="mergesort").copy()

    # читаемые подписи: <orig><pos><mut>, с цепью при необходимости
    def make_label(r):
        chain = (str(r.get("chain") or "")).strip()
        pos = int(r["residue_number"])
        return f"{chain}{r['original']}{pos}{r['mutated']}" if chain else f"{r['original']}{pos}{r['mutated']}"
    df["label"] = df.apply(make_label, axis=1)

    # X как индексы, чтобы подписи не «съезжали»
    x = range(len(df))
    y = pd.to_numeric(df[col], errors="coerce")

    plt.figure(figsize=(11, 6))
    plt.bar(x, y, alpha=0.8)
    plt.xticks(x, df["label"], rotation=45, ha="right")
    plt.title(title)
    plt.xlabel("Mutation")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(out_file)
    plt.close()
    print(f"Saved plot: {out_file}")


def main(input_csv, out_dir="plots"):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(input_csv)

    # RMSD
    plot_metrics(
        df,
        "rmsd",
        title="RMSD for single-point mutations",
        ylabel="RMSD (Å)",
        out_file=os.path.join(
            out_dir,
            "mutation_rmsd.png"
        )
    )

    # COM shift
    plot_metrics(
        df,
        "com_shift",
        title="Center-of-mass shift for mutations",
        ylabel="ΔCOM (Å)",
        out_file=os.path.join(
            out_dir,
            "mutation_com_shift.png"
        )
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Visualize mutation metrics"
    )
    p.add_argument(
        "input_csv",
        nargs="?",
        default="mutation_results.csv",
        help=(
            "CSV с результатами run_mutation_batch.py "
            "(по умолчанию mutation_results.csv)"
        )
    )
    p.add_argument(
        "--out-dir",
        default="plots",
        help="куда сохранять графики"
    )
    args = p.parse_args()

    main(args.input_csv, args.out_dir)
