"""Run local micro-benchmarks for qrpt AEAD hot paths."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from timeit import repeat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def bench(stmt: str, setup: str, label: str, *, number: int, reps: int) -> None:
    runs = repeat(stmt=stmt, setup=setup, number=number, repeat=reps)
    best = min(runs)
    avg_ms = (best / number) * 1000
    print(f"{label:38s} best={best:.4f}s ({avg_ms:.3f} ms/op, n={number}, r={reps})")


def run_size_benches(size_bytes: int, label: str, number: int, reps: int) -> None:
    setup = (
        "from qrpt import encrypt_with_shared_secret,decrypt_with_shared_secret;"
        "s=b'x'*32;a=b'ctx';"
        f"p=os.urandom({size_bytes});"
        "n,c=encrypt_with_shared_secret(p,s,aad=a)"
    )
    setup = "import os;" + setup

    bench(
        stmt="encrypt_with_shared_secret(p,s,aad=a)",
        setup=setup,
        label=f"encrypt {label}",
        number=number,
        reps=reps,
    )
    bench(
        stmt="decrypt_with_shared_secret(n,c,s,aad=a)",
        setup=setup,
        label=f"decrypt {label}",
        number=number,
        reps=reps,
    )


if __name__ == "__main__":
    try:
        import cryptography  # noqa: F401
    except Exception:
        print("SKIP: cryptography dependency not installed; benchmark not executed.")
        raise SystemExit(0)

    from qrpt import derive_aead_key

    bench(
        stmt="derive_aead_key(s)",
        setup="from qrpt import derive_aead_key; s=b'x'*32",
        label="HKDF derive_aead_key",
        number=5000,
        reps=5,
    )

    run_size_benches(256 * 1024, "256KB", number=100, reps=3)
    run_size_benches(1 * 1024 * 1024, "1MB", number=30, reps=3)
    run_size_benches(16 * 1024 * 1024, "16MB", number=3, reps=2)

    # 1GB benchmark is intentionally a small amount to avoid runaway runtime/memory.
    if os.environ.get("QRPT_RUN_1GB", "0") == "1":
        try:
            run_size_benches(1 * 1024 * 1024 * 1024, "1GB", number=1, reps=1)
        except MemoryError:
            print("SKIP: 1GB benchmark skipped due to insufficient memory.")
    else:
        print("SKIP: 1GB benchmark disabled by default. Set QRPT_RUN_1GB=1 to enable.")
