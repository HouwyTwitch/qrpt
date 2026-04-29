from .exceptions import DependencyError

try:
    import oqs
except Exception as exc:  # pragma: no cover
    oqs = None
    _oqs_error = exc
else:
    _oqs_error = None


def require_oqs():
    if oqs is None:
        raise DependencyError("Missing `oqs` dependency.") from _oqs_error
    return oqs


def load_aesgcm():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except Exception as exc:  # pragma: no cover
        raise DependencyError("Missing `cryptography` dependency.") from exc
    return AESGCM


def derive_hkdf_sha384(shared_secret: bytes, length: int, info: bytes) -> bytes:
    try:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    except Exception as exc:  # pragma: no cover
        raise DependencyError("Missing `cryptography` dependency.") from exc
    return HKDF(algorithm=hashes.SHA384(), length=length, salt=None, info=info).derive(shared_secret)
