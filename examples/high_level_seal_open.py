from qrpt import generate_kem_keypair, seal_to_public_key, open_with_secret_key

receiver = generate_kem_keypair()
payload = seal_to_public_key(b"top secret", receiver.public_key, aad=b"session-42")
print(open_with_secret_key(payload, receiver.secret_key))
