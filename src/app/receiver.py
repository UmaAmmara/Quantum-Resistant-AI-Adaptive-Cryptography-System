"""
Member B — Day 4 (corrected)
Chat app — RECEIVER side.

This matches Member A's chat_app_sender.py exactly:
- Same host/port (127.0.0.1:65432)
- Same length-prefixed socket protocol (8 bytes = length, then JSON payload)
- Same JSON keys: variant_used, ciphertext_kem, encrypted_message, nonce, public_key
- Same base64 encoding for binary fields

Flow:
1. Listen for an incoming connection
2. Receive the JSON payload, base64-decode the binary fields
3. Decapsulate the Kyber shared secret using our OWN keypair
   (NOTE: see the important setup note below about key exchange)
4. Decrypt the AES-GCM message using that shared secret
5. Run telemetry through attack_detector.pkl to check for anomalies
"""

import socket
import json
import base64
import time
import joblib
import pandas as pd
import oqs
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HOST = "127.0.0.1"
PORT = 65432

detector = joblib.load("attack_detector.pkl")


def check_for_attack(data_size_bytes: int, elapsed_ms: float, simulate_suspicious: bool = False) -> str:
    """
    Runs the Isolation Forest attack detector on this transaction's telemetry.
    Uses the SAME 7 features the model was trained on:
    data_size_bytes, latency_ms, cpu_load_percent, available_memory_mb,
    key_size_bytes, output_size_bytes, time_taken_ms

    If simulate_suspicious=True, injects values far outside the normal
    training range (e.g. an extreme decrypt time and CPU load) to
    demonstrate the detector actually firing "ATTACK DETECTED" — useful
    for the demo/report, since real benign traffic rarely looks like this.
    """
    import psutil

    if simulate_suspicious:
        # Values chosen to sit well outside the benchmark dataset's normal
        # range (e.g. repeated-failure / brute-force-probe-like pattern):
        # extremely high "decrypt time" and abnormal CPU load relative to
        # a tiny payload — a pattern that shouldn't occur in legitimate use.
        cpu_load = 99.5
        available_mb = 50.0
        elapsed_ms = 5000.0
    else:
        cpu_load = psutil.cpu_percent(interval=0.1)
        available_mb = psutil.virtual_memory().available / (1024 * 1024)

    row = pd.DataFrame([[
        data_size_bytes, elapsed_ms, cpu_load, available_mb,
        0, 0, elapsed_ms
    ]], columns=["data_size_bytes", "latency_ms", "cpu_load_percent",
                 "available_memory_mb", "key_size_bytes",
                 "output_size_bytes", "time_taken_ms"])

    prediction = detector.predict(row)
    return "NORMAL" if prediction[0] == 1 else "ATTACK DETECTED"


def recv_exact(conn: socket.socket, num_bytes: int) -> bytes:
    """Reads exactly num_bytes from the socket (handles partial reads)."""
    buf = b""
    while len(buf) < num_bytes:
        chunk = conn.recv(num_bytes - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed before expected data arrived")
        buf += chunk
    return buf


def handle_connection(conn: socket.socket):
    # Step 1: read the 8-byte length header
    length_header = recv_exact(conn, 8)
    payload_length = int.from_bytes(length_header, "big")

    # Step 2: read exactly that many bytes — this is our JSON payload
    payload_bytes = recv_exact(conn, payload_length)
    payload = json.loads(payload_bytes.decode("utf-8"))

    print("\n" + "=" * 50)
    print("MESSAGE RECEIVED")
    print("=" * 50)

    variant_used = payload["variant_used"]
    ciphertext_kem = base64.b64decode(payload["ciphertext_kem"])
    encrypted_message = base64.b64decode(payload["encrypted_message"])
    nonce = base64.b64decode(payload["nonce"])
    sender_public_key = base64.b64decode(payload["public_key"])
    sender_secret_key = base64.b64decode(payload["secret_key"])

    start = time.time()

    # DEMO SIMPLIFICATION (see sender's docstring note):
    # A real receiver would hold its OWN secret key, generated locally,
    # and the sender would have encapsulated against the receiver's public
    # key. Here, the sender generated the keypair itself, so we import that
    # same secret key to correctly decapsulate. This is not how a real
    # deployment should work — it exists only to demonstrate the encrypt/
    # decrypt pipeline within a single-process prototype.
    with oqs.KeyEncapsulation(variant_used, secret_key=sender_secret_key) as kem:
        shared_secret = kem.decap_secret(ciphertext_kem)

    aes_key = shared_secret[:32]
    aesgcm = AESGCM(aes_key)

    try:
        decrypted_message = aesgcm.decrypt(nonce, encrypted_message, None)
        decryption_ok = True
    except Exception as e:
        print(f"[WARNING] Decryption failed: {e}")
        decrypted_message = b""
        decryption_ok = False

    elapsed_ms = (time.time() - start) * 1000
    data_size = len(encrypted_message)

    print(f"Algorithm    : {variant_used}")
    print(f"Message      : {decrypted_message.decode('utf-8', errors='replace')}")
    print(f"Size         : {data_size} bytes")
    print(f"Decrypt time : {elapsed_ms:.2f} ms")
    print(f"Decryption   : {'VALID' if decryption_ok else 'FAILED'}")

    # The sender can flag a transaction as suspicious (e.g. a simulated
    # brute-force probe) to demonstrate the detector actually firing.
    simulate_suspicious = payload.get("simulate_attack", False)
    status = check_for_attack(data_size, elapsed_ms, simulate_suspicious=simulate_suspicious)
    print(f"AI status    : {status}")
    print("=" * 50)


def run_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[RECEIVER] Listening on {HOST}:{PORT} ... waiting for sender")

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"[RECEIVER] Connected by {addr}")
                handle_connection(conn)


if __name__ == "__main__":
    run_receiver()