import hashlib

from database.db import Secret
from cryptography.fernet import Fernet

cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)

async def generate_hash(secret: str) -> str:
    secret_key = hashlib.sha256(secret.encode())

    return secret_key.hexdigest()


async def validate_secret_key(secret_key: str, code_phrase: str = '') -> bool:
    code_phrase = await generate_hash(code_phrase)

    secret_document = await Secret.find_one({'secret_key': secret_key})

    if secret_document is not None and secret_document['code_phrase'] == code_phrase:
        return True

    return False


async def generate_crypto_secret(secret: str) -> bytes:
    return cipher.encrypt(bytes(secret, 'utf-8'))


async def decrypt_crypto_secret(encrypted_text: bytes) -> str:
    return cipher.decrypt(encrypted_text).decode('utf-8')
