from qrpt import generate_sig_keypair, sign_message, verify_message

kp = generate_sig_keypair()
msg = b"release-artifact-digest"
sig = sign_message(msg, kp.secret_key, kp.algorithm)
print("verified:", verify_message(msg, sig, kp.public_key, kp.algorithm))
