from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

## https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#key-loading

def sign_game_state(priv_key:rsa.RSAPrivateKey, game_state) -> bytes:
    signature = priv_key.sign(
        game_state,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def generate_private_key() -> rsa.RSAPrivateKey:
    private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend())
    
    return private_key

def verify_signature(public_key:rsa.RSAPublicKey, game_state, signature:bytes):
    return public_key.verify(
        signature,
        game_state,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )


