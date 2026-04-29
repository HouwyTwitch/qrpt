# qrpt

Post-quantum cryptography toolkit with a safer, modular architecture.

## What's improved (optimization + safety)
- Reduced unnecessary bytes copying in AEAD hot paths using `to_bytes()` fast-path for `bytes` input.
- Enabled `slots=True` on public dataclasses for lower object overhead.
- Kept strict input validation and nonce-length checks.
- Added repeatable benchmark runner for timing regressions.

## Quick benchmark
```bash
PYTHONPATH=. python benchmarks/timeit_suite.py
```

## Direct timeit commands
```bash
PYTHONPATH=. python -m timeit -s 'from qrpt import derive_aead_key; s=b"x"*32' 'derive_aead_key(s)'
PYTHONPATH=. python -m timeit -s 'from qrpt import encrypt_with_shared_secret; s=b"x"*32; p=b"a"*1024; a=b"ctx"' 'encrypt_with_shared_secret(p,s,aad=a)'
PYTHONPATH=. python -m timeit -s 'from qrpt import encrypt_with_shared_secret,decrypt_with_shared_secret; s=b"x"*32; p=b"a"*1024; a=b"ctx"; n,c=encrypt_with_shared_secret(p,s,aad=a)' 'decrypt_with_shared_secret(n,c,s,aad=a)'
```

## Package layout
- `qrpt/constants.py`, `qrpt/exceptions.py`, `qrpt/types.py`
- `qrpt/backends.py` (backend loading)
- `qrpt/kem.py`, `qrpt/signatures.py`, `qrpt/aead.py`
- `qrpt/payload.py`, `qrpt/highlevel.py`, `qrpt/validators.py`
- `benchmarks/timeit_suite.py`

## Examples
```bash
python examples/key_exchange_and_encrypt.py
python examples/sign_and_verify.py
python examples/high_level_seal_open.py
```

## Test
```bash
PYTHONPATH=. pytest -q
```
