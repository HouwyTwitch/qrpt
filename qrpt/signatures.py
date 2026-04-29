from .backends import require_oqs
from .constants import DEFAULT_SIG
from .types import SigKeypair
from .validators import require_nonempty_bytes


def generate_sig_keypair(algorithm: str = DEFAULT_SIG) -> SigKeypair:
    oqs = require_oqs()
    with oqs.Signature(algorithm) as sig:
        return SigKeypair(algorithm, sig.generate_keypair(), sig.export_secret_key())


def sign_message(message: bytes, secret_key: bytes, algorithm: str = DEFAULT_SIG) -> bytes:
    require_nonempty_bytes("message", message)
    require_nonempty_bytes("secret_key", secret_key)
    oqs = require_oqs()
    with oqs.Signature(algorithm, secret_key=secret_key) as sig:
        return sig.sign(message)


def verify_message(message: bytes, signature: bytes, public_key: bytes, algorithm: str = DEFAULT_SIG) -> bool:
    require_nonempty_bytes("message", message)
    require_nonempty_bytes("signature", signature)
    require_nonempty_bytes("public_key", public_key)
    oqs = require_oqs()
    with oqs.Signature(algorithm) as sig:
        return bool(sig.verify(message, signature, public_key))
