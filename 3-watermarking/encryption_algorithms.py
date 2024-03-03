# Caesar Cipher
def caesar_encrypt(plaintext, shift):
    encrypted = ""
    for char in plaintext:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                start = ord('a')
                encrypted += chr((ord(char) - start + shift_amount) % 26 + start)
            else:
                start = ord('A')
                encrypted += chr((ord(char) - start + shift_amount) % 26 + start)
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

# Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    key_length = len(key)
    ciphertext = ''
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length].lower()) - ord('a')  # Calcul du décalage pour chaque caractère
            encrypted_char = caesar_encrypt(char, shift)
            ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    key_length = len(key)
    plaintext = ''
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length].lower()) - ord('a')  # Calcul du décalage pour chaque caractère
            decrypted_char = caesar_decrypt(char, shift)
            plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext
