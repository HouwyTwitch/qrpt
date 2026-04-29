import os
from .backends import derive_hkdf_sha384, load_aesgcm
from .constants import KEY_SIZE, NONCE_SIZE
from .validators import require_bytes, to_bytes


def derive_aead_key(shared_secret: bytes, context: bytes = b"qrpt-v1") -> bytes:
    require_bytes("shared_secret", shared_secret)
    require_bytes("context", context)
    return derive_hkdf_sha384(to_bytes(shared_secret), KEY_SIZE, to_bytes(context))


def encrypt_with_shared_secret(plaintext: bytes, shared_secret: bytes, *, aad: bytes = b"") -> tuple[bytes, bytes]:
    require_bytes("plaintext", plaintext)
    require_bytes("shared_secret", shared_secret)
    require_bytes("aad", aad)
    AESGCM = load_aesgcm()
    key = derive_aead_key(shared_secret)
    nonce = os.urandom(NONCE_SIZE)
    return nonce, AESGCM(key).encrypt(nonce, to_bytes(plaintext), to_bytes(aad))


def decrypt_with_shared_secret(nonce: bytes, ciphertext: bytes, shared_secret: bytes, *, aad: bytes = b"") -> bytes:
    require_bytes("nonce", nonce)
    require_bytes("ciphertext", ciphertext)
    require_bytes("shared_secret", shared_secret)
    require_bytes("aad", aad)
    if len(nonce) != NONCE_SIZE:
        raise ValueError("nonce must be exactly 12 bytes for AES-GCM.")
    AESGCM = load_aesgcm()
    key = derive_aead_key(shared_secret)
    return AESGCM(key).decrypt(to_bytes(nonce), to_bytes(ciphertext), to_bytes(aad))
