from qrpt import generate_kem_keypair, encapsulate, decapsulate, encrypt_with_shared_secret, decrypt_with_shared_secret

bob = generate_kem_keypair()
kem_ct, alice_secret = encapsulate(bob.public_key)
bob_secret = decapsulate(bob.secret_key, kem_ct)
nonce, ct = encrypt_with_shared_secret(b"message", alice_secret, aad=b"chat")
print(decrypt_with_shared_secret(nonce, ct, bob_secret, aad=b"chat"))
