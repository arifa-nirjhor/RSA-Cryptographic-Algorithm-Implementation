
from pathlib import Path
from getpass import getpass
from math import lcm

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keys(folder_name, password):

    # Step 1: Create directory
    key_directory = Path(folder_name)
    key_directory.mkdir(parents=True, exist_ok=True)

    private_path = key_directory / "private_key.pem"
    public_path = key_directory / "public_key.pem"

    # Prevent overwriting existing keys
    if private_path.exists() or public_path.exists():
        raise FileExistsError(
            "Key files already exist. Choose another folder."
        )

    # Step 2: Generate RSA-3072 private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=3072
    )

    # Step 3: Generate public key
    public_key = private_key.public_key()

    # Step 4: Serialize encrypted private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            password.encode("utf-8")
        )
    )

    # Step 5: Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Step 6: Save keys
    with private_path.open("xb") as file:
        file.write(private_pem)

    with public_path.open("xb") as file:
        file.write(public_pem)

    # Step 7: Extract mathematical parameters
    private_numbers = private_key.private_numbers()
    public_numbers = public_key.public_numbers()

    p = private_numbers.p
    q = private_numbers.q
    d = private_numbers.d
    e = public_numbers.e
    n = public_numbers.n

    lambda_n = lcm(p - 1, q - 1)

    # Step 8: Display key information
    print("\n===== RSA KEY INFORMATION =====")
    print("Key Size:", private_key.key_size, "bits")
    print("Public Exponent (e):", e)
    print("Modulus Size:", n.bit_length(), "bits")

    # Step 9: Mathematical verification
    print("\n===== MATHEMATICAL VERIFICATION =====")
    print("n = p * q:", n == p * q)
    print("(e * d) mod lambda(n):", (e * d) % lambda_n)

    # Step 10: Display saved file locations
    print("\n===== KEY FILES =====")
    print("Private Key:", private_path.resolve())
    print("Public Key:", public_path.resolve())

    return private_path, public_path


def main():

    print("===== RSA-3072 KEY GENERATION =====")

    folder_name = input(
        "Enter folder name to save keys [keys]: "
    ).strip()

    if not folder_name:
        folder_name = "keys"

    password = getpass(
        "Enter password to protect private key: "
    )

    confirm_password = getpass(
        "Confirm password: "
    )

    if not password:
        print("Error: Password cannot be empty.")
        return

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    try:
        generate_rsa_keys(folder_name, password)
        print("\nRSA-3072 key generation successful!")

    except (OSError, ValueError) as error:
        print("\nKey generation failed:", error)


if __name__ == "__main__":
    main()
