from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def generate_key():
    return os.urandom(16)

def encrypt(plain_text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    padded_data = pad(plain_text.encode('utf-8'), AES.block_size)
    cipher_text = cipher.encrypt(padded_data)
    return cipher.iv + cipher_text

def decrypt(cipher_data, key):
    iv = cipher_data[:16]
    actual_cipher_text = cipher_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(actual_cipher_text)
    plain_text = unpad(decrypted_padded, AES.block_size)
    return plain_text.decode('utf-8')

if __name__ == "__main__":
    key = generate_key()
    message = "Bao cao Mon An toan va Bao mat Thong tin - 2026"

    print("--- DEMO CHƯƠNG TRÌNH MÃ HÓA AES ---")
    print(f"Văn bản gốc: {message}")

    encrypted_data = encrypt(message, key)
    print(f"Dữ liệu mã hóa (Hex): {encrypted_data.hex()}")

    decrypted_message = decrypt(encrypted_data, key)
    print(f"Văn bản giải mã: {decrypted_message}")
