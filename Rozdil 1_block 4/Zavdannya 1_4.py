from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import os
import base64

print("--- Демонстрація криптографічних алгоритмів ---")
message = b"Це дуже секретне повідомлення"

# 1. Хешування (SHA-256) - незворотній процес
print("\n1. Хешування (SHA-256):")
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(message)
hash_value = digest.finalize()
print(f"   Оригінал: {message}")
print(f"   SHA-256 хеш (base64): {base64.b64encode(hash_value).decode()}")

# 2. Симетричне шифрування (AES) - зворотній процес
print("\n2. Симетричне шифрування (AES-256 CBC):")
key = os.urandom(32)
iv = os.urandom(16)

padder = sym_padding.PKCS7(128).padder()
padded_data = padder.update(message) + padder.finalize()

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted = encryptor.update(padded_data) + encryptor.finalize()
print(f"   Зашифровано (base64): {base64.b64encode(encrypted).decode()}")

decryptor = cipher.decryptor()
decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
unpadder = sym_padding.PKCS7(128).unpadder()
decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
print(f"   Розшифровано: {decrypted.decode()}")

# 3. Асиметрична криптографія та цифровий підпис (RSA)
print("\n3. Асиметрична криптографія (RSA):")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

print("   --- Цифровий підпис ---")
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print(f"   Підпис (base64): {base64.b64encode(signature).decode()}")

try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("   Перевірка підпису: УСПІШНО (підпис валідний)")
except Exception as e:
    print(f"   Перевірка підпису: ПОМИЛКА ({e})")