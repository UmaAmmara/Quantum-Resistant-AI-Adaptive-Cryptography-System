"""
Dilithium (ML-DSA) digital signature test: sign a message and verify it.

This script:
1. Generates a Dilithium keypair
2. Signs a test message
3. Verifies the signature
4. Also tests that a tampered message correctly FAILS verification
"""

import oqs

# Dilithium variants standardized by NIST as ML-DSA
DILITHIUM_VARIANTS = ["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"]


def test_dilithium_variant(variant_name: str):
    print(f"\n--- Testing {variant_name} ---")

    with oqs.Signature(variant_name) as signer:
        public_key = signer.generate_keypair()

        message = b"Hello from Member B - this message is signed by Dilithium"
        signature = signer.sign(message)

        print(f"Public key size: {len(public_key)} bytes")
        print(f"Signature size: {len(signature)} bytes")

        # Verify with a fresh Signature object (simulating the receiver)
        with oqs.Signature(variant_name) as verifier:
            is_valid = verifier.verify(message, signature, public_key)
            print(f"Signature valid for original message: {is_valid}")
            assert is_valid, "Signature verification failed unexpectedly!"

            # Now tamper with the message and confirm verification FAILS
            tampered_message = b"Hello from Member B - this message has been tampered!"
            is_valid_tampered = verifier.verify(tampered_message, signature, public_key)
            print(f"Signature valid for tampered message (should be False): {is_valid_tampered}")
            assert not is_valid_tampered, "Tampered message should NOT verify!"

    return {
        "variant": variant_name,
        "public_key_size": len(public_key),
        "signature_size": len(signature),
    }


if __name__ == "__main__":
    print("Available signature mechanisms (showing first 10):", oqs.get_enabled_sig_mechanisms()[:10])

    results = []
    for variant in DILITHIUM_VARIANTS:
        result = test_dilithium_variant(variant)
        results.append(result)

    print("\n=== Summary ===")
    for r in results:
        print(r)