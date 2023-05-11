import hashlib
import time
import json

def generate_token(input_str):
    # Generate a unique token using the input string and timestamp
    timestamp = str(time.time()).encode('utf-8')
    input_str = input_str.encode('utf-8')
    unique_bytes = hashlib.sha256(timestamp + input_str).digest()[:16]
    unique_str = unique_bytes.hex()[:16]

    # Return the token
    return unique_str