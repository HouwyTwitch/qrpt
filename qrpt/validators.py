from .exceptions import PayloadError


def require_bytes(name: str, value: bytes) -> None:
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes-like.")


def require_nonempty_bytes(name: str, value: bytes) -> None:
    require_bytes(name, value)
    if len(value) == 0:
        raise PayloadError(f"{name} must not be empty.")


def to_bytes(value: bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    return bytes(value)
