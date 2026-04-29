from .backends import require_oqs
from .constants import DEFAULT_KEM
from .types import KemKeypair
from .validators import require_nonempty_bytes


def generate_kem_keypair(algorithm: str = DEFAULT_KEM) -> KemKeypair:
    oqs = require_oqs()
    with oqs.KeyEncapsulation(algorithm) as kem:
        return KemKeypair(algorithm, kem.generate_keypair(), kem.export_secret_key())


def encapsulate(public_key: bytes, algorithm: str = DEFAULT_KEM) -> tuple[bytes, bytes]:
    require_nonempty_bytes("public_key", public_key)
    oqs = require_oqs()
    with oqs.KeyEncapsulation(algorithm) as kem:
        return kem.encap_secret(public_key)


def decapsulate(secret_key: bytes, kem_ciphertext: bytes, algorithm: str = DEFAULT_KEM) -> bytes:
    require_nonempty_bytes("secret_key", secret_key)
    require_nonempty_bytes("kem_ciphertext", kem_ciphertext)
    oqs = require_oqs()
    with oqs.KeyEncapsulation(algorithm, secret_key=secret_key) as kem:
        return kem.decap_secret(kem_ciphertext)
