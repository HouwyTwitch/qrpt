import pytest
from qrpt.aead import decrypt_with_shared_secret
from qrpt.highlevel import open_with_secret_key, seal_to_public_key


def test_decrypt_rejects_bad_nonce_len():
    with pytest.raises(ValueError):
        decrypt_with_shared_secret(b"short", b"x", b"y" * 32)


def test_seal_rejects_non_bytes_plaintext():
    with pytest.raises(TypeError):
        seal_to_public_key("not-bytes", b"pk")  # type: ignore[arg-type]


def test_open_rejects_empty_inputs():
    with pytest.raises(Exception):
        open_with_secret_key(b"", b"")
