"""
Member A — Day 3
Key-size escalation logic: when a threat is detected (by Member B's
attack_detector.py), this module forces the system to switch from a
lighter Kyber variant up to the strongest one (ML-KEM-1024), even at
a performance cost.

This is the crypto-side half of the closed feedback loop described in
the roadmap: AI/detector says "escalate" -> this module enforces it.
"""

import oqs
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Ordered from lightest to strongest — escalation always moves RIGHT in this list
KYBER_ESCALATION_LEVELS = ["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"]


class AdaptiveKyberEngine:
    """
    Wraps Kyber encryption with an escalation policy. Normal operation uses
    whatever the AI model recommends (Day 4 will wire this up). If a threat
    is flagged, this engine overrides that recommendation and forces the
    maximum security level, exactly as the roadmap's Attack Detection
    Module -> AI Optimization Layer override describes.
    """

    def __init__(self, default_level: str = "ML-KEM-512"):
        if default_level not in KYBER_ESCALATION_LEVELS:
            raise ValueError(f"Unknown Kyber level: {default_level}")
        self.current_level = default_level
        self.threat_active = False

    def escalate(self):
        """Force the maximum security level immediately."""
        self.current_level = KYBER_ESCALATION_LEVELS[-1]  # ML-KEM-1024
        self.threat_active = True
        print(f"[ESCALATION] Threat detected — switching to {self.current_level}")

    def de_escalate(self):
        """Return to normal AI-recommended behavior once the threat clears."""
        self.threat_active = False
        print("[DE-ESCALATION] Threat cleared — AI recommendations re-enabled")

    def set_level(self, recommended_level: str):
        """
        Called by Day 4's pipeline with the AI model's recommendation.
        If a threat is currently active, this call is IGNORED — the
        escalation always wins, exactly like the roadmap specifies.
        """
        if self.threat_active:
            print(f"[OVERRIDE] AI recommended {recommended_level}, but threat is active. "
                  f"Staying at {self.current_level}.")
            return
        if recommended_level not in KYBER_ESCALATION_LEVELS:
            raise ValueError(f"Unknown Kyber level: {recommended_level}")
        self.current_level = recommended_level
        print(f"[NORMAL] Using AI-recommended level: {self.current_level}")

    def encrypt_message(self, message: bytes) -> dict:
        """Encrypts a message using whatever level is currently active."""
        variant = self.current_level

        with oqs.KeyEncapsulation(variant) as receiver:
            public_key = receiver.generate_keypair()
            secret_key = receiver.export_secret_key()

            with oqs.KeyEncapsulation(variant) as sender:
                ciphertext, shared_secret = sender.encap_secret(public_key)

            aes_key = shared_secret[:32]
            aesgcm = AESGCM(aes_key)
            nonce = os.urandom(12)
            encrypted = aesgcm.encrypt(nonce, message, None)

            shared_secret_check = receiver.decap_secret(ciphertext)
            assert shared_secret_check == shared_secret

        return {
            "variant_used": variant,
            "ciphertext_kem": ciphertext,
            "encrypted_message": encrypted,
            "nonce": nonce,
            "public_key": public_key,
            "secret_key": secret_key,
        }


if __name__ == "__main__":
    engine = AdaptiveKyberEngine(default_level="ML-KEM-512")

    print("--- Normal operation (AI recommends ML-KEM-768) ---")
    engine.set_level("ML-KEM-768")
    result = engine.encrypt_message(b"Routine message under normal conditions")
    print(f"Used: {result['variant_used']}\n")

    print("--- Attack detected! ---")
    engine.escalate()
    result = engine.encrypt_message(b"Message sent while under suspected attack")
    print(f"Used: {result['variant_used']}\n")

    print("--- AI tries to recommend a lighter level mid-attack (should be ignored) ---")
    engine.set_level("ML-KEM-512")
    result = engine.encrypt_message(b"Another message, still under attack")
    print(f"Used: {result['variant_used']}\n")

    print("--- Threat clears, normal operation resumes ---")
    engine.de_escalate()
    engine.set_level("ML-KEM-512")
    result = engine.encrypt_message(b"Back to normal conditions")
    print(f"Used: {result['variant_used']}")