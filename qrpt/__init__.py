"""qrpt: post-quantum crypto toolkit for Python.

Provides:
- AEAD helpers
- KEM wrappers
- Signature wrappers
- Payload serialization helpers
- High-level seal/open API
"""

from .aead import decrypt_with_shared_secret, derive_aead_key, encrypt_with_shared_secret
from .constants import DEFAULT_KEM, DEFAULT_SIG
from .exceptions import DependencyError, PayloadError, QrptError
from .highlevel import open_with_secret_key, seal_to_public_key
from .kem import decapsulate, encapsulate, generate_kem_keypair
from .payload import deserialize_payload, serialize_payload
from .signatures import generate_sig_keypair, sign_message, verify_message
from .types import EncryptedEnvelope, KemKeypair, SigKeypair
