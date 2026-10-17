
from pathlib import Path
from getpass import getpass

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidKey


# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Existing key and ciphertext paths
PRIVATE_KEY_PATH = BASE_DIR / "keys" / "private_key.pem"
CIPHERTEXT_PATH = BASE_DIR / "encrypted_message.bin"


def load_private_key(password):

    # Step 1: Read encrypted private key
    with open(PRIVATE_KEY_PATH, "rb") as file:
        private_key_data = file.read()

    # Step 2: Deserialize private key
    private_key = serialization.load_pem_private_key(
        private_key_data,
        password=password.encode("utf-8")
    )

    # Step 3: Verify RSA key type
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise ValueError("The provided key is not an RSA private key.")

    return private_key


def rsa_decrypt(ciphertext, private_key):

    # Step 4: Decrypt using RSA-OAEP
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext_bytes


def main():

    print("===== RSA-3072 OAEP DECRYPTION =====")

    try:
        # Step 5: Ask for private key password
        password = getpass(
            "Enter your private key password: "
        )

        # Step 6: Load private key
        private_key = load_private_key(password)

        # Step 7: Read ciphertext
        with open(CIPHERTEXT_PATH, "rb") as file:
            ciphertext = file.read()

        # Step 8: Decrypt ciphertext
        plaintext_bytes = rsa_decrypt(
            ciphertext,
            private_key
        )

        # Step 9: Convert bytes to string
        plaintext = plaintext_bytes.decode("utf-8")

        # Step 10: Display results
        print("\n===== DECRYPTION RESULTS =====")
        print("Algorithm: RSA-OAEP")
        print("Key Size:", private_key.key_size, "bits")
        print("Hash Algorithm: SHA-256")

        print("Ciphertext Size:", len(ciphertext), "bytes")
        print("Plaintext Size:", len(plaintext_bytes), "bytes")

        print("\nRecovered Plaintext:")
        print(plaintext)

        print("\nDecryption Successful!")

    except FileNotFoundError as error:
        print("\nRequired file not found:", error)

    except (ValueError, TypeError, InvalidKey):
        print(
            "\nDecryption failed. Check the password, "
            "private key, ciphertext, and OAEP settings."
        )

    except UnicodeDecodeError:
        print("\nDecryption succeeded, but plaintext is not valid UTF-8.")


if __name__ == "__main__":
    main()
