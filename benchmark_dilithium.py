"""
Member B — Day 2
Benchmark Dilithium (ML-DSA) across multiple data sizes and network conditions,
logging every result into data/dataset.csv using the SAME shared schema
that Member A's Kyber benchmark uses (see setup_project.py).

This combines: dilithium_test.py (Day 1) + telemetry_collector.py (Day 1)
+ setup_project.py's append_row (Day 1) into one benchmarking run.
"""

import oqs
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from telemetry_collector import get_cpu_load, get_memory_info, simulate_network_latency_ms
from setup_project import append_row, DATASET_COLUMNS

DILITHIUM_VARIANTS = ["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"]

# Same five data sizes as Member A, so results are directly comparable
DATA_SIZES = {
    "1KB": 1 * 1024,
    "10KB": 10 * 1024,
    "100KB": 100 * 1024,
    "1MB": 1 * 1024 * 1024,
    "5MB": 5 * 1024 * 1024,
}

NETWORK_CONDITIONS = ["fast", "normal", "slow", "very_slow"]

DATASET_PATH = os.path.join("data", "dataset.csv")


def run_dilithium_once(variant_name: str, data_size_bytes: int, network_condition: str) -> dict:
    """Runs one full Dilithium sign + verify cycle over a message of the target size and times it."""

    start_time = time.perf_counter()
    success = 1

    try:
        with oqs.Signature(variant_name) as signer:
            public_key = signer.generate_keypair()

            # Message of the target size (signature schemes sign a hash internally,
            # but we still want to measure signing cost over realistic payload sizes)
            message = os.urandom(data_size_bytes)
            signature = signer.sign(message)

            with oqs.Signature(variant_name) as verifier:
                is_valid = verifier.verify(message, signature, public_key)
                assert is_valid

            key_size_bytes = len(public_key)
            output_size_bytes = len(signature)

    except Exception as e:
        print(f"  [ERROR] {variant_name} @ {data_size_bytes} bytes failed: {e}")
        success = 0
        key_size_bytes = 0
        output_size_bytes = 0

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    # Same telemetry collection Member A uses, for consistency
    cpu_load = get_cpu_load(sample_seconds=0.1)
    mem_info = get_memory_info()
    latency_ms = simulate_network_latency_ms(network_condition)

    row = {
        "algorithm": variant_name,
        "algorithm_type": "signature",
        "data_size_bytes": data_size_bytes,
        "network_condition": network_condition,
        "latency_ms": latency_ms,
        "cpu_load_percent": cpu_load,
        "available_memory_mb": mem_info["available_mb"],
        "key_size_bytes": key_size_bytes,
        "output_size_bytes": output_size_bytes,
        "time_taken_ms": elapsed_ms,
        "success": success,
        "best_choice_label": "",  # filled in later during Phase 3 labeling
    }
    return row


def run_full_benchmark():
    total_runs = len(DILITHIUM_VARIANTS) * len(DATA_SIZES) * len(NETWORK_CONDITIONS)
    print(f"Running {total_runs} Dilithium benchmark combinations...\n")

    count = 0
    for variant in DILITHIUM_VARIANTS:
        for size_label, size_bytes in DATA_SIZES.items():
            for condition in NETWORK_CONDITIONS:
                row = run_dilithium_once(variant, size_bytes, condition)
                append_row(DATASET_PATH, row)
                count += 1
                print(f"[{count}/{total_runs}] {variant} | {size_label:6s} | {condition:9s} "
                      f"-> {row['time_taken_ms']} ms")

    print(f"\nDone. {count} rows appended to {DATASET_PATH}")


if __name__ == "__main__":
    if not os.path.exists(DATASET_PATH):
        print("dataset.csv not found — run setup_project.py first!")
        sys.exit(1)

    run_full_benchmark()