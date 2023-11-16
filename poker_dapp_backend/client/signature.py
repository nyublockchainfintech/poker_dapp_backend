from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


class KeyGenerator:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.private_key: rsa.RSAPrivateKey
        self.public_key: rsa.RSAPublicKey
        self.generate_keys()

    def generate_keys(self):
        # Generate a private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=self.key_size
        )

        # Generate public key
        self.public_key = self.private_key.public_key()

    def serialize_private_key(self, filename="private_key.pem"):
        # Serialize private key
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        with open(filename, "wb") as f:
            f.write(private_pem)

    def serialize_public_key(self, filename="public_key.pem"):
        # Serialize public key
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        with open(filename, "wb") as f:
            f.write(public_pem)


class KeySigner:
    def __init__(self, private_key_file):
        self.private_key_file = private_key_file
        self.private_key = self.load_private_key()

    def load_private_key(self) -> rsa.RSAPrivateKey:
        # Load the private key from a file
        with open(self.private_key_file, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None
            )
            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise TypeError("Expected an RSAPrivateKey")
            return private_key

    def sign_message(self, message) -> bytes:
        signature = self.private_key.sign(
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32),
            hashes.SHA256(),
        )
        return signature
