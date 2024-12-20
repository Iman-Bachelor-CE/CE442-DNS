#!/usr/bin/env python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii

key = get_random_bytes(16)
iv = get_random_bytes(16)

def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = bytes(data, 'utf-8')
    enc = cipher.encrypt(pad(data, 16, style='pkcs7'))
    return enc

def decrypt_data(encryptedParams):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptedParams = bytes.fromhex(encryptedParams)
    paddedParams = cipher.decrypt(encryptedParams)
    return unpad(paddedParams, 16, style='pkcs7')

print('You know how CBC bit flipping works?')
msg = "crypto0"
print("Current Message is: " + msg)
print("Encryption of Message in hex: ", end=" ")
print((iv + encrypt_data(msg)).hex())

enc_msg = input("Give me Encrypted msg in hex: ")
try:
    final_dec_msg = decrypt_data(enc_msg)
    print(final_dec_msg)
    if bytes("crypto1", "utf-8") in final_dec_msg:
        print('Whoa!! Your attack works!')
    else:
        print('Try again you can do it!!')
    exit()
except:
    print('bye bye!!')
#output
#You know how CBC bit flipping works ?
# Current Message i s : crypto0
# Encryption of Message in hex :
#(NOTE : The iv and key values ​​are random, so the output will change each time.)	ee6d003abe8021f417b06281d3e5489598a22c1d3f86aa9b8fca69dc232a919f
# Give me Encrypted msg in hex :