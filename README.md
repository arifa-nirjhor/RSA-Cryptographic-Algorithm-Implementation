# RSA Cryptographic Algorithm Implementation in Python

![Python](https://img.shields.io/badge/Python-3.14.6-blue?logo=python) ![Cryptography](https://img.shields.io/badge/Library-cryptography-informational) ![RSA](https://img.shields.io/badge/RSA-3072-success) ![Purpose](https://img.shields.io/badge/Purpose-Educational%20%26%20Research-lightgrey)

An educational Python project exploring the **mathematical foundations of RSA** and implementing **RSA-3072 public-key encryption and decryption with OAEP-SHA-256** using the [`cryptography`](https://cryptography.io/) library.

The project progresses from number theory exercises to practical key generation, encrypted private-key storage, and message encryption/decryption. It also serves as preparatory work for a future **AES-256-GCM + RSA-3072 hybrid encryption** experiment; hybrid encryption is **not implemented in this repository**.

## Features

- Interactive, user-input-driven implementations of fundamental number theory algorithms.
- RSA-3072 key generation with public exponent **65537**.
- Password-encrypted **PKCS#8 PEM** private-key serialization and **SubjectPublicKeyInfo PEM** public-key serialization.
- RSA-OAEP encryption/decryption with **SHA-256** and **MGF1(SHA-256)**.
- Ciphertext saved as a binary file and printed in Base64 during encryption.
- Mathematical key consistency checks: `n == p * q` and `(e * d) % lcm(p - 1, q - 1) == 1`.

## Project files

The following names match the supplied Python scripts. Put the scripts at the repository root, or adjust paths/imports if you reorganize them.

```text
RSA-Cryptographic-Algorithm-Implementation/
├── prime_factorization.py
├── Eulers'_Totient_Finction.py
├── Fermat's_Factorization.py
├── GCD_Euclidean_Algorithm.py
├── Modular_Arithmetic.py
├── extended_euclidean.py
├── modular_inverse.py
├── binary_modular_exponentiation.py
├── miller_rabin.py
├── rsa_key_generation.py
├── rsa_encryption.py
├── rsa_decryption.py
├── .gitignore
└── README.md

# Generated locally (ignored by Git):
# keys/private_key.pem
# keys/public_key.pem
# encrypted_message.bin
# .venv/
```

### Mathematical foundations

| File | Implementation | Key idea |
| --- | --- | --- |
| `prime_factorization.py` | Trial-division factorization | Find prime factors of an integer. |
| `Eulers'_Totient_Finction.py` | Euler's totient | Compute `φ(n)` by removing prime-factor contributions. |
| `Fermat's_Factorization.py` | Fermat factorization | Search for `n = x² − y² = (x − y)(x + y)`. |
| `GCD_Euclidean_Algorithm.py` | Euclidean algorithm | Compute `gcd(a, b)`. |
| `Modular_Arithmetic.py` | Modular operations | Addition, subtraction, multiplication, exponentiation, inverse. |
| `extended_euclidean.py` | Extended Euclidean algorithm | Find `x, y` with `ax + by = gcd(a, b)`. |
| `modular_inverse.py` | Modular multiplicative inverse | Find `a⁻¹ mod m` when `gcd(a, m) = 1`. |
| `binary_modular_exponentiation.py` | Square-and-multiply | Compute `aᵇ mod n` efficiently. |
| `miller_rabin.py` | Probabilistic primality test | Detect composites using repeated modular-exponentiation tests. |

These scripts are **learning implementations**, not production cryptographic primitives. In particular, the Miller–Rabin module is not used to generate RSA keys; key generation is delegated to `cryptography`.

### Practical RSA modules

| File | Function |
| --- | --- |
| `rsa_key_generation.py` | Generate a 3072-bit key pair, encrypt the private-key PEM with a user-provided password, and save both PEM files. |
| `rsa_encryption.py` | Load `keys/public_key.pem`, encrypt a user-entered UTF-8 message using RSA-OAEP, and write `encrypted_message.bin`. |
| `rsa_decryption.py` | Load `keys/private_key.pem` using the password, decrypt `encrypted_message.bin`, and display the recovered UTF-8 plaintext. |

## Cryptographic design

**Key generation**

For distinct primes `p` and `q`:

```text
n = p × q
λ(n) = lcm(p − 1, q − 1)
e = 65537
e × d ≡ 1 (mod λ(n))
Public key:  (n, e)
Private key: (n, d) plus additional RSA parameters
```

The library securely generates and validates the key pair; the project checks these relationships after generation.

**Encryption / decryption**

```text
User message (UTF-8)
       │
       ▼
RSA-3072 public key + OAEP(SHA-256, MGF1-SHA-256)
       │
       ▼
encrypted_message.bin (384 bytes)
       │
       ▼
RSA-3072 private key + matching OAEP parameters
       │
       ▼
Recovered UTF-8 message
```

OAEP is randomized, so encrypting the same plaintext twice normally produces different ciphertexts.

### Message size limit

For a 3072-bit RSA key and OAEP with SHA-256:

```text
Maximum plaintext = 384 − 2 × 32 − 2 = 318 bytes
Ciphertext size   = 384 bytes
```

The **318-byte limit is measured in UTF-8 bytes**, not characters. This direct-RSA example is intended for short messages; larger data should use authenticated symmetric encryption with RSA protecting only a session key.

## Getting started

### Prerequisites

- Python **3.14.6** (development environment used for this project; other compatible versions may work)
- `pip`
- The Python [`cryptography`](https://pypi.org/project/cryptography/) package

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/RSA-Cryptographic-Algorithm-Implementation.git
cd RSA-Cryptographic-Algorithm-Implementation
```

Replace `YOUR-USERNAME` with your GitHub username and use the actual repository URL.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use `Set-ExecutionPolicy -Scope Process RemoteSigned` for the current terminal session, or run `.\.venv\Scripts\python.exe` directly without activating.

### 3. Install dependencies

```powershell
python -m pip install cryptography
```

### 4. Generate your RSA key pair

```powershell
python rsa_key_generation.py
```

At the prompts, press **Enter** to select the default `keys` directory, then enter and confirm a strong private-key password. Keep this password safe. The program will create:

```text
keys/public_key.pem
keys/private_key.pem
```

Do not rerun key generation into an existing key directory: the program intentionally refuses to overwrite existing key files.

### 5. Encrypt a short message

```powershell
python rsa_encryption.py
```

Example interaction:

```text
===== RSA-3072 OAEP ENCRYPTION =====
Enter message to encrypt: Hello RSA
...
Ciphertext Size: 384 bytes
...
Encryption Successful!
```

The binary ciphertext is saved to `encrypted_message.bin` in the same directory as `rsa_encryption.py`. Each encryption run overwrites that file.

### 6. Decrypt the ciphertext

```powershell
python rsa_decryption.py
```

Enter the password used during key generation. For the preceding example, the recovered plaintext should be:

```text
Recovered Plaintext:
Hello RSA

Decryption Successful!
```

Run all three RSA scripts from the **repository root** so that key generation's default `keys/` directory matches the paths expected by the encryption and decryption scripts.

## Run the mathematical exercises

Each exercise prompts for input. Examples:

```powershell
python prime_factorization.py
python GCD_Euclidean_Algorithm.py
python extended_euclidean.py
python modular_inverse.py
python binary_modular_exponentiation.py
python miller_rabin.py
```

`modular_inverse.py` imports `extended_gcd` from `extended_euclidean.py`, so those files must be in the same importable directory.

For the filenames containing an apostrophe, quote the path in PowerShell:

```powershell
python "Eulers'_Totient_Finction.py"
python "Fermat's_Factorization.py"
```

## Suggested manual checks

| Scenario | Expected behavior |
| --- | --- |
| Generate a new RSA key pair | 3072-bit modulus and exponent 65537; key consistency checks pass. |
| Encrypt and decrypt a short UTF-8 message | Recovered message matches original. |
| Encrypt the same message twice | Ciphertext normally differs because OAEP is randomized. |
| Enter more than 318 UTF-8 bytes | Encryption rejects the message. |
| Enter an incorrect private-key password | Private-key loading fails. |
| Alter ciphertext or use the wrong private key | OAEP decryption fails. |

These are **recommended checks**, not claims of a completed automated test suite or formal security audit.

## Security notes

- **Never commit `private_key.pem`**, private-key passwords, or real secrets. The public key may be shared, but this project excludes the entire generated `keys/` directory by default.
- Treat the uploaded/generated key pair as **development-only**. Generate fresh keys for any new use, especially if a private key has been shared or exposed.
- RSA-OAEP provides confidentiality for short messages; it does **not** provide sender authentication or digital signatures.
- RSA-3072 provides classical security, **not post-quantum security**.
- Mathematical implementations are for education; use established cryptographic libraries for actual key generation and encryption.
- Do not claim performance, cryptanalytic resistance, or production readiness without separate testing and review.

## Roadmap

- [x] Mathematical foundation implementations
- [x] RSA-3072 key generation module
- [x] RSA-OAEP-SHA256 encryption module
- [x] RSA-OAEP-SHA256 decryption module
- [ ] Automated tests and reproducible benchmarks
- [ ] AES-256-GCM + RSA-3072 hybrid encryption (separate future project)

## References

- [Python `cryptography` — RSA](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
- [RFC 8017 — PKCS #1: RSA Cryptography Specifications](https://www.rfc-editor.org/rfc/rfc8017)
- [NIST SP 800-57 Part 1 — Key Management Recommendations](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)

## Project status

**Educational and research-oriented implementation.** Source files include interactive mathematical exercises and practical RSA-3072 scripts. Automated tests and performance benchmarks are not included in the supplied files.
