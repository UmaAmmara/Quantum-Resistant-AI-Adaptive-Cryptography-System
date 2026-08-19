"""
Member A — Day 2
Basic exploratory data analysis (EDA) on dataset.csv using pandas.
Run this AFTER benchmark_kyber.py has populated the dataset, and ideally
after Member B's Dilithium results are merged in too.

Produces a few simple charts saved into results/ so the team can see
patterns before moving to Phase 3 (AI model training).
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # so it works in headless Codespaces without a display
import matplotlib.pyplot as plt
import os

DATASET_PATH = os.path.join("data", "dataset.csv")
RESULTS_DIR = "results"


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    print(f"Loaded {len(df)} rows from {DATASET_PATH}")
    print(f"Columns: {list(df.columns)}")
    return df


def basic_summary(df: pd.DataFrame):
    print("\n--- Row counts per algorithm ---")
    print(df["algorithm"].value_counts())

    print("\n--- Success rate ---")
    print(df["success"].value_counts(normalize=True) * 100)

    print("\n--- Average time_taken_ms per algorithm ---")
    print(df.groupby("algorithm")["time_taken_ms"].mean().round(3))


def chart_time_vs_datasize(df: pd.DataFrame):
    """Line chart: how does time scale with data size, per algorithm?"""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    pivot = df.groupby(["algorithm", "data_size_bytes"])["time_taken_ms"].mean().reset_index()

    plt.figure(figsize=(8, 5))
    for algo in pivot["algorithm"].unique():
        subset = pivot[pivot["algorithm"] == algo].sort_values("data_size_bytes")
        plt.plot(subset["data_size_bytes"], subset["time_taken_ms"], marker="o", label=algo)

    plt.xscale("log")
    plt.xlabel("Data size (bytes, log scale)")
    plt.ylabel("Average time taken (ms)")
    plt.title("Encryption time vs. data size, by algorithm")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "time_vs_datasize.png")
    plt.savefig(out_path)
    print(f"Saved chart: {out_path}")
    plt.close()


def chart_time_vs_network(df: pd.DataFrame):
    """Bar chart: how does network condition affect total time?"""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    pivot = df.groupby(["algorithm", "network_condition"])["time_taken_ms"].mean().reset_index()
    pivot_wide = pivot.pivot(index="network_condition", columns="algorithm", values="time_taken_ms")

    # Order conditions from fast to very_slow for a readable chart
    order = ["fast", "normal", "slow", "very_slow"]
    pivot_wide = pivot_wide.reindex([c for c in order if c in pivot_wide.index])

    pivot_wide.plot(kind="bar", figsize=(8, 5))
    plt.ylabel("Average time taken (ms)")
    plt.title("Time taken by network condition and algorithm")
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "time_vs_network.png")
    plt.savefig(out_path)
    print(f"Saved chart: {out_path}")
    plt.close()


if __name__ == "__main__":
    df = load_dataset()
    basic_summary(df)
    chart_time_vs_datasize(df)
    chart_time_vs_network(df)
    print("\nEDA complete. Check the results/ folder for charts.")