"""
1. Generates a Kyber keypair (for 512, 768, and 1024 variants)
2. Performs key encapsulation/decapsulation to derive a shared secret
3. Uses that shared secret to encrypt/decrypt a short test message (AES via the secret)
"""

import oqs
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# The three Kyber security levels we will let the AI choose between later
KYBER_VARIANTS = ["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"]


def test_kyber_variant(variant_name: str):
    print(f"\n--- Testing {variant_name} ---")

    # Receiver generates a keypair
    with oqs.KeyEncapsulation(variant_name) as receiver:
        public_key = receiver.generate_keypair()

        # Sender encapsulates a shared secret using the receiver's public key
        with oqs.KeyEncapsulation(variant_name) as sender:
            ciphertext, shared_secret_sender = sender.encap_secret(public_key)

        # Receiver decapsulates to get the same shared secret
        shared_secret_receiver = receiver.decap_secret(ciphertext)

        assert shared_secret_sender == shared_secret_receiver, "Shared secrets do not match!"
        print(f"Shared secret established. Length: {len(shared_secret_sender)} bytes")
        print(f"Public key size: {len(public_key)} bytes")
        print(f"Ciphertext size: {len(ciphertext)} bytes")

        # Use the shared secret (first 32 bytes) as an AES-256-GCM key
        aes_key = shared_secret_sender[:32]
        aesgcm = AESGCM(aes_key)
        nonce = os.urandom(12)

        message = b"Hello from Member A - this message is protected by Kyber + AES-GCM"
        encrypted = aesgcm.encrypt(nonce, message, None)
        decrypted = aesgcm.decrypt(nonce, encrypted, None)

        assert decrypted == message, "Decryption failed!"
        print(f"Message encrypted/decrypted successfully: {decrypted.decode()}")

    return {
        "variant": variant_name,
        "public_key_size": len(public_key),
        "ciphertext_size": len(ciphertext),
        "shared_secret_size": len(shared_secret_sender),
    }


if __name__ == "__main__":
    print("Available KEM mechanisms (showing first 10):", oqs.get_enabled_kem_mechanisms()[:10])

    results = []
    for variant in KYBER_VARIANTS:
        result = test_kyber_variant(variant)
        results.append(result)

    print("\n=== Summary ===")
    for r in results:
        print(r)