from .aead import decrypt_with_shared_secret, encrypt_with_shared_secret
from .constants import DEFAULT_KEM, PAYLOAD_VERSION
from .kem import decapsulate, encapsulate
from .payload import deserialize_payload, serialize_payload
from .types import EncryptedEnvelope
from .validators import require_nonempty_bytes, require_bytes, to_bytes


def seal_to_public_key(plaintext: bytes, receiver_public_key: bytes, *, algorithm: str = DEFAULT_KEM, aad: bytes = b"") -> bytes:
    require_bytes("plaintext", plaintext)
    require_nonempty_bytes("receiver_public_key", receiver_public_key)
    require_bytes("aad", aad)
    kem_ct, shared_secret = encapsulate(receiver_public_key, algorithm)
    nonce, ciphertext = encrypt_with_shared_secret(plaintext, shared_secret, aad=aad)
    return serialize_payload(EncryptedEnvelope(PAYLOAD_VERSION, algorithm, kem_ct, nonce, ciphertext, to_bytes(aad)))


def open_with_secret_key(payload: bytes, receiver_secret_key: bytes) -> bytes:
    require_nonempty_bytes("payload", payload)
    require_nonempty_bytes("receiver_secret_key", receiver_secret_key)
    env = deserialize_payload(payload)
    shared_secret = decapsulate(receiver_secret_key, env.kem_ciphertext, env.kem_algorithm)
    return decrypt_with_shared_secret(env.nonce, env.ciphertext, shared_secret, aad=env.aad)
