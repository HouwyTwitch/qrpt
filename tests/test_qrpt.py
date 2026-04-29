import json
import pytest

from qrpt.constants import PAYLOAD_VERSION
from qrpt.exceptions import PayloadError
from qrpt.payload import deserialize_payload


def test_rejects_wrong_version():
    p = {"v": PAYLOAD_VERSION + 1, "kem": "ML-KEM-768", "kem_ct": "", "nonce": "AAAAAAAAAAAAAAAA", "ct": "", "aad": ""}
    with pytest.raises(PayloadError):
        deserialize_payload(json.dumps(p).encode())


def test_rejects_missing_keys():
    with pytest.raises(PayloadError):
        deserialize_payload(b'{"v":1}')
