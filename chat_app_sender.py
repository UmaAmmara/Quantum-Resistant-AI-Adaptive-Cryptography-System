"""
Member A — Day 4
Chat app — SENDER side, with live AI decision hookup.

Flow:
1. Collect telemetry (data size, latency, cpu load, memory)
2. Ask the trained Random Forest model (ai_model.pkl) which Kyber variant to use
3. Encrypt the message using that recommendation (via AdaptiveKyberEngine)
4. Send ciphertext + public key + nonce + metadata to the receiver over a socket

Run the receiver (Member B's script) FIRST, then run this sender script.
"""

import socket
import json
import base64
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from telemetry_collector import get_cpu_load, get_memory_info, simulate_network_latency_ms
from key_escalation import AdaptiveKyberEngine
from train_model import predict_best_algorithm

HOST = "127.0.0.1"   # localhost — change to receiver's IP if on different machines
PORT = 65432
MODEL_PATH = os.path.join("models", "ai_model.pkl")


def get_ai_recommendation(data_size_bytes: int, network_condition: str) -> str:
    """
    Collects current telemetry and asks the Random Forest model which
    Kyber variant to use for an encryption operation.
    """
    cpu_load = get_cpu_load(sample_seconds=0.2)
    mem_info = get_memory_info()
    latency_ms = simulate_network_latency_ms(network_condition)

    telemetry = {
        "data_size_bytes": data_size_bytes,
        "latency_ms": latency_ms,
        "cpu_load_percent": cpu_load,
        "available_memory_mb": mem_info["available_mb"],
        "algorithm_type": "encryption",
    }

    recommended = predict_best_algorithm(telemetry, MODEL_PATH)
    print(f"[AI] Telemetry: {telemetry}")
    print(f"[AI] Recommended algorithm: {recommended}")
    return recommended


def send_message(message: str, network_condition: str = "normal", simulate_attack: bool = False):
    """
    Encrypts and sends one message to the receiver.
    If simulate_attack=True, forces escalation to max security (ML-KEM-1024)
    regardless of what the AI recommends — used to test Day 4's attack demo.

    NOTE (demo simplification): In a real two-party KEM exchange, the
    RECEIVER generates the keypair and shares only the public key with the
    sender beforehand; the receiver alone holds the secret key and never
    transmits it. For this prototype, the sender generates the keypair
    itself, so the secret key is also sent over the socket so the receiver
    can decapsulate. This is NOT secure for a real deployment — it exists
    only so this single-process demo can show the full encrypt/decrypt
    pipeline. Document this clearly as a limitation in the final report.
    """
    message_bytes = message.encode("utf-8")
    data_size = len(message_bytes)

    engine = AdaptiveKyberEngine(default_level="ML-KEM-512")

    if simulate_attack:
        engine.escalate()
    else:
        recommended = get_ai_recommendation(data_size, network_condition)
        engine.set_level(recommended)

    result = engine.encrypt_message(message_bytes)

    # Package everything the receiver needs into JSON (binary fields base64-encoded)
    payload = {
        "variant_used": result["variant_used"],
        "ciphertext_kem": base64.b64encode(result["ciphertext_kem"]).decode(),
        "encrypted_message": base64.b64encode(result["encrypted_message"]).decode(),
        "nonce": base64.b64encode(result["nonce"]).decode(),
        "public_key": base64.b64encode(result["public_key"]).decode(),
        "secret_key": base64.b64encode(result["secret_key"]).decode(),  # demo-only, see note above
        "simulate_attack": simulate_attack,  # tells the receiver to demo the attack-detector firing
    }
    payload_json = json.dumps(payload).encode("utf-8")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Send length header first, then the payload, so the receiver knows
        # exactly how many bytes to read (important for larger messages)
        s.sendall(len(payload_json).to_bytes(8, "big"))
        s.sendall(payload_json)
        print(f"[SENDER] Sent message using {result['variant_used']} "
              f"({len(payload_json)} bytes over the wire)")


if __name__ == "__main__":
    print("=== Sender Demo ===\n")

    print("--- Normal message, AI chooses algorithm ---")
    send_message("Hello, this is a normal secure message.", network_condition="normal")

    print("\n--- Large message under poor network conditions ---")
    send_message("A" * 5000, network_condition="slow")

    print("\n--- Simulated attack scenario: forced max security ---")
    send_message("This message is sent while under attack.", simulate_attack=True)