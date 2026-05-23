from cryptography.fernet import Fernet
import base64
import hashlib

from .config import settings


def _derive_key(master_key: str) -> bytes:
    key = hashlib.sha256(master_key.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_api_key(plain_text: str) -> str:
    key = _derive_key(settings.master_key)
    f = Fernet(key)
    return f.encrypt(plain_text.encode()).decode()


def decrypt_api_key(encrypted: str) -> str:
    key = _derive_key(settings.master_key)
    f = Fernet(key)
    return f.decrypt(encrypted.encode()).decode()
