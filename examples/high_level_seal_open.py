from qrpt import DependencyError, generate_kem_keypair, open_with_secret_key, seal_to_public_key

try:
    receiver = generate_kem_keypair()
    payload = seal_to_public_key(b"top secret", receiver.public_key, aad=b"session-42")
    print(open_with_secret_key(payload, receiver.secret_key))
except DependencyError as exc:
    print("Dependency setup issue:", exc)
    print("Tip: install Open Quantum Safe Python bindings for PQC features.")
