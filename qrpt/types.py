from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KemKeypair:
    algorithm: str
    public_key: bytes
    secret_key: bytes


@dataclass(frozen=True, slots=True)
class SigKeypair:
    algorithm: str
    public_key: bytes
    secret_key: bytes


@dataclass(frozen=True, slots=True)
class EncryptedEnvelope:
    version: int
    kem_algorithm: str
    kem_ciphertext: bytes
    nonce: bytes
    ciphertext: bytes
    aad: bytes
