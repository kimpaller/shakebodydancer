import hashlib
import random
import string

class Utility():

    def generate_random_hash():
        # Generate a random string of 16 characters
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Create a SHA-256 hash object
        hash_object = hashlib.sha256(random_string.encode())
        
        # Get the hexadecimal representation of the hash
        hash_hex = hash_object.hexdigest()
        
        return hash_hex
