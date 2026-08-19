"""
Member B — Day 1
Dataset schema design + project folder structure setup.

This defines the exact CSV columns that Phase 2 (benchmarking) will fill in,
and creates the folder layout the whole team will use for the rest of the project.

Run this once to scaffold the project folders and create an empty dataset
file with the correct headers ready to be appended to.
"""

import os
import csv

# ---- 1. Define the dataset schema ----
# Every row in dataset.csv will follow this exact column order.
# This is the single source of truth both Member A and Member B
# must use when logging benchmark results in Phase 2.

DATASET_COLUMNS = [
    "algorithm",          # e.g. "ML-KEM-512", "ML-DSA-65"
    "algorithm_type",      # "encryption" (Kyber) or "signature" (Dilithium)
    "data_size_bytes",     # size of payload being processed
    "network_condition",   # "fast" | "normal" | "slow" | "very_slow"
    "latency_ms",          # simulated network latency
    "cpu_load_percent",    # system CPU load at time of test
    "available_memory_mb", # available system memory at time of test
    "key_size_bytes",       # public key size for this algorithm
    "output_size_bytes",    # ciphertext size (encryption) or signature size (signature)
    "time_taken_ms",         # how long the operation took
    "success",                # 1 if operation succeeded, 0 if it failed
    "best_choice_label",       # filled in later: the algorithm that performed BEST
                                 # for this exact condition set (the AI's training label)
]


def create_empty_dataset(path: str):
    """Creates dataset.csv with just the header row, ready for Phase 2 to append to."""
    with open(path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(DATASET_COLUMNS)
    print(f"Created empty dataset with headers at: {path}")


def append_row(path: str, row: dict):
    """
    Appends a single result row to dataset.csv.
    'row' must be a dict using exactly the keys in DATASET_COLUMNS.
    Phase 2's benchmark scripts will call this function repeatedly.
    """
    with open(path, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=DATASET_COLUMNS)
        writer.writerow(row)


# ---- 2. Project folder structure ----
PROJECT_FOLDERS = [
    "crypto",       # crypto_engine.py, signature.py
    "telemetry",    # telemetry_collector.py
    "data",         # dataset.csv lives here
    "models",       # ai_model.pkl, attack_detector.pkl
    "app",          # chat_app.py, demo.py
    "results",      # final charts, comparison tables, screenshots
]


def scaffold_project(root: str = "."):
    """Creates the folder structure for the rest of the project."""
    for folder in PROJECT_FOLDERS:
        folder_path = os.path.join(root, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")


if __name__ == "__main__":
    print("--- Scaffolding project folders ---")
    scaffold_project(root=".")

    print("\n--- Creating empty dataset with schema ---")
    dataset_path = os.path.join("data", "dataset.csv")
    create_empty_dataset(dataset_path)

    print("\n--- Schema columns (for reference) ---")
    for col in DATASET_COLUMNS:
        print(f"  - {col}")

    print("\n--- Testing append_row with a sample (fake) entry ---")
    sample_row = {
        "algorithm": "ML-KEM-768",
        "algorithm_type": "encryption",
        "data_size_bytes": 1024,
        "network_condition": "normal",
        "latency_ms": 45.2,
        "cpu_load_percent": 23.5,
        "available_memory_mb": 4096.0,
        "key_size_bytes": 1184,
        "output_size_bytes": 1088,
        "time_taken_ms": 1.8,
        "success": 1,
        "best_choice_label": "",  # left blank — filled in during Phase 3 labeling
    }
    append_row(dataset_path, sample_row)
    print("Sample row appended. Check data/dataset.csv to confirm.")