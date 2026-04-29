# qrpt

Post-quantum cryptography toolkit with a safer, modular architecture.

## What's improved (optimization + safety)
- Reduced unnecessary bytes copying in AEAD hot paths using `to_bytes()` fast-path for `bytes` input.
- Enabled `slots=True` on public dataclasses for lower object overhead.
- Kept strict input validation and nonce-length checks.
- Added repeatable benchmark runner for timing regressions.

## Quick benchmark
```bash
python benchmarks/timeit_suite.py
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


## Running tests locally (Windows/Linux/macOS)
Use one of these:
```bash
python -m pytest -q
```
or install editable first:
```bash
pip install -e .
pytest -q
```


## Windows compatibility
- Base install works on Windows with Python 3.11+ using:
```bash
pip install .
```
- Post-quantum KEM/signature features depend on `oqs` and native `liboqs`, which may require extra setup on Windows. Install optional PQC deps with:
```bash
pip install .[pqc]
```
- AEAD-only helpers (`derive_aead_key`, `encrypt_with_shared_secret`, `decrypt_with_shared_secret`) work without `oqs`.


## Benchmark data sizes
The benchmark suite now includes randomized payload sizes for:
- 256KB
- 1MB
- 16MB
- 1GB (small amount, disabled by default)

Run:
```bash
python benchmarks/timeit_suite.py
```
Enable 1GB case:
```bash
QRPT_RUN_1GB=1 python benchmarks/timeit_suite.py
```


## Sample benchmark results
Example output from `python benchmarks/timeit_suite.py`:

```text
HKDF derive_aead_key                   best=0.0348s (0.007 ms/op, n=5000, r=5)
encrypt 256KB                          best=0.0068s (0.068 ms/op, n=100, r=3)
decrypt 256KB                          best=0.0068s (0.068 ms/op, n=100, r=3)
encrypt 1MB                            best=0.0124s (0.412 ms/op, n=30, r=3)
decrypt 1MB                            best=0.0124s (0.413 ms/op, n=30, r=3)
encrypt 16MB                           best=0.0175s (5.826 ms/op, n=3, r=2)
decrypt 16MB                           best=0.0183s (6.102 ms/op, n=3, r=2)
```


## Troubleshooting `oqs` on Windows
If you see errors like `module oqs has no attribute KeyEncapsulation`, your installed `oqs` package is not the expected Open Quantum Safe binding.

- Uninstall conflicting package(s):
```bash
pip uninstall oqs
```
- Install the correct Open Quantum Safe Python binding + native liboqs per your platform docs.

The examples now catch `DependencyError` and print a friendly hint instead of a raw traceback.
