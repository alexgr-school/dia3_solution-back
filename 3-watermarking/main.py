from PIL import Image
import numpy as np

from encryption_algorithms import vigenere_encrypt, vigenere_decrypt

def prepare_image(image_path):
    image = Image.open(image_path)
    return np.array(image), image.mode

def apply_lsb(array_image, message):
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'  # Ending signal
    index = 0
    for value in np.nditer(array_image, op_flags=['readwrite']):
        if index < len(binary_message):
            value[...] = (value - value % 2) + int(binary_message[index])
            index += 1
        else:
            break
    return array_image

def extract_lsb(array_image):
    binary_message = ''.join(str(value % 2) for value in np.nditer(array_image))
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '00000000':  # Check for ending signal
            break
        message += chr(int(byte, 2))
    return message

def lsb1(image_path, message, password):
    array_image, mode = prepare_image(image_path)
    encrypted_message = vigenere_encrypt(message, password)
    watermarked_array = apply_lsb(array_image, encrypted_message)
    watermarked_image = Image.fromarray(watermarked_array.astype(np.uint8), mode)
    watermarked_image.save('output.png')

def extract_message(watermarked_image_path, password):
    array_image, mode = prepare_image(watermarked_image_path)
    encrypted_message = extract_lsb(array_image)
    message = vigenere_decrypt(encrypted_message, password)
    print(message)


# Exemple d'utilisation
if __name__ == "__main__":
    password = "secret"
    print("Création de l'image avec message caché")
    lsb1(image_path="./input.png", message="Nous avons bien manger aujourd'hui !", password=password)
    
    print("Extraction du message de l'image")
    extract_message(watermarked_image_path="output.png", password=password)
