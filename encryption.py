from cryptography.fernet import Fernet
import bcrypt
import os

KEY_FILE = "key.key"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key

key = load_or_create_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def hash_master_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_master_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
