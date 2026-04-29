from qrpt import (
    DependencyError,
    decapsulate,
    decrypt_with_shared_secret,
    encapsulate,
    encrypt_with_shared_secret,
    generate_kem_keypair,
)

try:
    bob = generate_kem_keypair()
    kem_ct, alice_secret = encapsulate(bob.public_key)
    bob_secret = decapsulate(bob.secret_key, kem_ct)
    nonce, ct = encrypt_with_shared_secret(b"message", alice_secret, aad=b"chat")
    print(decrypt_with_shared_secret(nonce, ct, bob_secret, aad=b"chat"))
except DependencyError as exc:
    print("Dependency setup issue:", exc)
    print("Tip: install Open Quantum Safe Python bindings for PQC features.")
