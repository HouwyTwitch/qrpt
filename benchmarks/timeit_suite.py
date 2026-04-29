"""Run local micro-benchmarks for qrpt hot paths that do not require oqs."""

from __future__ import annotations

import sys
from pathlib import Path
from timeit import repeat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def bench(stmt: str, setup: str, label: str) -> None:
    runs = repeat(stmt=stmt, setup=setup, number=5000, repeat=5)
    best = min(runs)
    avg_us = (best / 5000) * 1_000_000
    print(f"{label:30s} best={best:.4f}s ({avg_us:.2f} us/op)")


if __name__ == "__main__":
    try:
        import cryptography  # noqa: F401
    except Exception:
        print("SKIP: cryptography dependency not installed; benchmark not executed.")
        raise SystemExit(0)

    bench(
        stmt="derive_aead_key(s)",
        setup="from qrpt import derive_aead_key; s=b'x'*32",
        label="HKDF derive_aead_key",
    )
    bench(
        stmt="encrypt_with_shared_secret(p,s,aad=a)",
        setup="from qrpt import encrypt_with_shared_secret; s=b'x'*32; p=b'a'*1024; a=b'ctx'",
        label="AESGCM encrypt 1KB",
    )
    bench(
        stmt="decrypt_with_shared_secret(n,c,s,aad=a)",
        setup="from qrpt import encrypt_with_shared_secret,decrypt_with_shared_secret; s=b'x'*32; p=b'a'*1024; a=b'ctx'; n,c=encrypt_with_shared_secret(p,s,aad=a)",
        label="AESGCM decrypt 1KB",
    )
