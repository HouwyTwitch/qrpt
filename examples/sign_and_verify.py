from qrpt import DependencyError, generate_sig_keypair, sign_message, verify_message

try:
    kp = generate_sig_keypair()
    msg = b"release-artifact-digest"
    sig = sign_message(msg, kp.secret_key, kp.algorithm)
    print("verified:", verify_message(msg, sig, kp.public_key, kp.algorithm))
except DependencyError as exc:
    print("Dependency setup issue:", exc)
    print("Tip: install Open Quantum Safe Python bindings for PQC features.")
