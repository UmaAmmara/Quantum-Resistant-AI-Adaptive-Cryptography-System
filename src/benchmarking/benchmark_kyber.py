"""
Member A — Day 2
Benchmark Kyber (ML-KEM) across multiple data sizes and network conditions,
logging every result into data/dataset.csv using the shared schema.

This combines: kyber_test.py (Day 1) + telemetry_collector.py (Day 1)
+ setup_project.py's append_row (Day 1) into one benchmarking run.
"""

import oqs
import time
import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Make sure we can import the Day 1 helper functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from telemetry_collector import get_cpu_load, get_memory_info, simulate_network_latency_ms
from setup_project import append_row, DATASET_COLUMNS

KYBER_VARIANTS = ["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"]

# Five data sizes from 1KB to 5MB, as the plan specifies
DATA_SIZES = {
    "1KB": 1 * 1024,
    "10KB": 10 * 1024,
    "100KB": 100 * 1024,
    "1MB": 1 * 1024 * 1024,
    "5MB": 5 * 1024 * 1024,
}

NETWORK_CONDITIONS = ["fast", "normal", "slow", "very_slow"]

DATASET_PATH = os.path.join("data", "dataset.csv")


def run_kyber_once(variant_name: str, data_size_bytes: int, network_condition: str) -> dict:
    """Runs one full Kyber encapsulation + AES encrypt/decrypt cycle and times it."""

    start_time = time.perf_counter()
    success = 1

    try:
        with oqs.KeyEncapsulation(variant_name) as receiver:
            public_key = receiver.generate_keypair()

            with oqs.KeyEncapsulation(variant_name) as sender:
                ciphertext, shared_secret_sender = sender.encap_secret(public_key)

            shared_secret_receiver = receiver.decap_secret(ciphertext)
            assert shared_secret_sender == shared_secret_receiver

            # Simulate encrypting a payload of the target size using the shared secret
            aes_key = shared_secret_sender[:32]
            aesgcm = AESGCM(aes_key)
            nonce = os.urandom(12)
            payload = os.urandom(data_size_bytes)  # random bytes standing in for real data

            encrypted = aesgcm.encrypt(nonce, payload, None)
            decrypted = aesgcm.decrypt(nonce, encrypted, None)
            assert decrypted == payload

            key_size_bytes = len(public_key)
            output_size_bytes = len(ciphertext)

    except Exception as e:
        print(f"  [ERROR] {variant_name} @ {data_size_bytes} bytes failed: {e}")
        success = 0
        key_size_bytes = 0
        output_size_bytes = 0

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    # Collect telemetry exactly like Day 1's telemetry_collector does
    cpu_load = get_cpu_load(sample_seconds=0.1)
    mem_info = get_memory_info()
    latency_ms = simulate_network_latency_ms(network_condition)

    row = {
        "algorithm": variant_name,
        "algorithm_type": "encryption",
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
    total_runs = len(KYBER_VARIANTS) * len(DATA_SIZES) * len(NETWORK_CONDITIONS)
    print(f"Running {total_runs} Kyber benchmark combinations...\n")

    count = 0
    for variant in KYBER_VARIANTS:
        for size_label, size_bytes in DATA_SIZES.items():
            for condition in NETWORK_CONDITIONS:
                row = run_kyber_once(variant, size_bytes, condition)
                append_row(DATASET_PATH, row)
                count += 1
                print(f"[{count}/{total_runs}] {variant} | {size_label:6s} | {condition:9s} "
                      f"-> {row['time_taken_ms']} ms")

    print(f"\nDone. {count} rows appended to {DATASET_PATH}")


if __name__ == "__main__":
    if not os.path.exists(DATASET_PATH):
        print("dataset.csv not found — run setup_project.py first!")
        sys.exit(1)

    # Run multiple repetitions so the combined dataset (Kyber + Dilithium)
    # comfortably clears the 400-row minimum. Each repeat captures fresh
    # timing/CPU noise, which is realistic and useful for the AI model.
    REPEATS = 4
    for i in range(REPEATS):
        print(f"\n=== Repeat run {i + 1}/{REPEATS} ===")
        run_full_benchmark()