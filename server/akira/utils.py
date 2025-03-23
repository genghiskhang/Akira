import base64
import os

def generate_secret(length):
    return base64.b32encode(os.urandom(length))[:length].decode('utf-8').lower()