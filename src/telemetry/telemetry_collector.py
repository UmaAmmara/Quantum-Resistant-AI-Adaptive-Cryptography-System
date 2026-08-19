"""
Member A — Day 1
Telemetry collector: captures system conditions (CPU load, available memory,
data size) that will later become the AI model's input features.

In the final system, this runs right before encryption happens, so the
AI model can decide which algorithm/parameter set fits current conditions.
"""

import psutil
import time


def get_cpu_load(sample_seconds: float = 0.5) -> float:
    """
    Returns current CPU utilization as a percentage (0-100).
    interval=sample_seconds means it measures usage over that window,
    which is more accurate than an instantaneous reading.
    """
    return psutil.cpu_percent(interval=sample_seconds)


def get_memory_info() -> dict:
    """Returns available and used memory in MB, plus percent used."""
    mem = psutil.virtual_memory()
    return {
        "available_mb": round(mem.available / (1024 * 1024), 2),
        "used_percent": mem.percent,
    }


def simulate_network_latency_ms(condition: str = "normal") -> float:
    """
    Simulates network latency since we don't have real network hardware
    to test against. 'condition' lets us generate different scenarios
    for the dataset (Phase 2 will loop through all of these).
    """
    import random
    latency_ranges = {
        "fast": (5, 20),       # e.g. local wifi / fiber
        "normal": (20, 80),    # e.g. average mobile/broadband
        "slow": (80, 250),     # e.g. congested or rural connection
        "very_slow": (250, 600),  # e.g. poor satellite/2G-like conditions
    }
    low, high = latency_ranges.get(condition, latency_ranges["normal"])
    return round(random.uniform(low, high), 2)


def collect_telemetry(data_size_bytes: int, network_condition: str = "normal") -> dict:
    """
    Main function: gathers a full telemetry snapshot.
    This dict shape is exactly what becomes one row in Phase 2's dataset,
    and exactly what the trained AI model will expect as input later.
    """
    cpu_load = get_cpu_load()
    mem_info = get_memory_info()
    latency_ms = simulate_network_latency_ms(network_condition)

    snapshot = {
        "data_size_bytes": data_size_bytes,
        "cpu_load_percent": cpu_load,
        "available_memory_mb": mem_info["available_mb"],
        "network_condition": network_condition,
        "latency_ms": latency_ms,
        "timestamp": time.time(),
    }
    return snapshot


if __name__ == "__main__":
    print("--- Single telemetry snapshot ---")
    snapshot = collect_telemetry(data_size_bytes=1024 * 50, network_condition="normal")
    for key, value in snapshot.items():
        print(f"{key}: {value}")

    print("\n--- Testing all network conditions ---")
    for condition in ["fast", "normal", "slow", "very_slow"]:
        snap = collect_telemetry(data_size_bytes=1024 * 100, network_condition=condition)
        print(f"{condition:10s} -> latency: {snap['latency_ms']} ms | cpu: {snap['cpu_load_percent']}%")