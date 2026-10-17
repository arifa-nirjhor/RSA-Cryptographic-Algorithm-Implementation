
from pathlib import Path
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


# File paths relative to this Python script
BASE_DIR = Path(__file__).resolve().parent

PUBLIC_KEY_PATH = BASE_DIR / "keys" / "public_key.pem"

CIPHERTEXT_PATH = BASE_DIR / "encrypted_message.bin"


def load_public_key():

    # Read public key from PEM file
    with open(PUBLIC_KEY_PATH, "rb") as file:
        public_key_data = file.read()

    # Deserialize public key
    public_key = serialization.load_pem_public_key(
        public_key_data
    )

    # Verify that this is an RSA public key
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("The provided key is not an RSA public key.")

    return public_key


def rsa_encrypt(message, public_key):

    # Convert plaintext into bytes
    message_bytes = message.encode("utf-8")

    # SHA-256 digest length = 32 bytes
    hash_length = hashes.SHA256().digest_size

    # Calculate maximum OAEP plaintext length
    max_length = (
        public_key.key_size // 8
        - 2 * hash_length
        - 2
    )

    if len(message_bytes) > max_length:
        raise ValueError(
            f"Message too long. Maximum size is "
            f"{max_length} bytes."
        )

    # Encrypt with RSA-OAEP and SHA-256
    ciphertext = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext


def main():

    print("===== RSA-3072 OAEP ENCRYPTION =====")

    try:
        # Step 1: Take message from user
        message = input("Enter message to encrypt: ")

        # Step 2: Load existing public key
        public_key = load_public_key()

        # Step 3: Encrypt message
        ciphertext = rsa_encrypt(message, public_key)

        # Step 4: Save encrypted data
        with open(CIPHERTEXT_PATH, "wb") as file:
            file.write(ciphertext)

        # Step 5: Convert ciphertext to Base64
        encoded_ciphertext = base64.b64encode(
            ciphertext
        ).decode("ascii")

        print("\n===== ENCRYPTION RESULTS =====")
        print("Algorithm: RSA-OAEP")
        print("Key Size:", public_key.key_size, "bits")
        print("Hash Algorithm: SHA-256")

        print("Plaintext:", message)
        print("Plaintext Size:", len(message.encode("utf-8")), "bytes")

        print("Ciphertext Size:", len(ciphertext), "bytes")

        print("\nCiphertext (Base64):")
        print(encoded_ciphertext)

        print("\nEncrypted file saved at:")
        print(CIPHERTEXT_PATH)

        print("\nEncryption Successful!")

    except (OSError, ValueError) as error:
        print("\nEncryption Failed:", error)


if __name__ == "__main__":
    main()
