import json
import random

# SUPER TOP SECRET NOT XOR ENCRYPTION HAPPENNING HERE
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=[]|:;<>?,.!@#$%^&*()'

def generate_key_encrypt(string):
    # :)
    key = ''.join(random.choice(letters) for i in range(len(string)))

    encoded = ""
    for p, k in zip(string, key):
        encoded += chr(ord(p) ^ ord(k))
    
    return encoded, key

def encrypt(string, key):
    encoded = ""
    for p, k in zip(string, key):
        encoded += chr(ord(p) ^ ord(k))
    
    return encoded

def decrypt(string, key):
    # LOL SAME THING AS ENCRYPT
    decoded = ""
    for p, k in zip(string, key):
        decoded += chr(ord(p) ^ ord(k))
    
    return decoded