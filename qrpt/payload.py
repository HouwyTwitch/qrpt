import base64
import json
from .constants import NONCE_SIZE, PAYLOAD_VERSION
from .exceptions import PayloadError
from .types import EncryptedEnvelope


def _b64e(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64d(data: str) -> bytes:
    try:
        return base64.b64decode(data.encode("ascii"), validate=True)
    except Exception as exc:
        raise PayloadError("Invalid base64 content.") from exc


def serialize_payload(envelope: EncryptedEnvelope) -> bytes:
    return json.dumps({
        "v": envelope.version,
        "kem": envelope.kem_algorithm,
        "kem_ct": _b64e(envelope.kem_ciphertext),
        "nonce": _b64e(envelope.nonce),
        "ct": _b64e(envelope.ciphertext),
        "aad": _b64e(envelope.aad),
    }, separators=(",", ":")).encode()


def deserialize_payload(payload: bytes) -> EncryptedEnvelope:
    try:
        obj = json.loads(payload.decode())
    except Exception as exc:
        raise PayloadError("Payload must be UTF-8 JSON bytes.") from exc
    required = {"v", "kem", "kem_ct", "nonce", "ct", "aad"}
    if set(obj.keys()) != required:
        raise PayloadError("Payload keys mismatch.")
    if obj["v"] != PAYLOAD_VERSION:
        raise PayloadError("Unsupported payload version.")
    nonce = _b64d(obj["nonce"])
    if len(nonce) != NONCE_SIZE:
        raise PayloadError("Invalid nonce length.")
    return EncryptedEnvelope(obj["v"], str(obj["kem"]), _b64d(obj["kem_ct"]), nonce, _b64d(obj["ct"]), _b64d(obj["aad"]))
