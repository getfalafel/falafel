from random import choice
import string

def generate_secret_key():
    """
    Generate a random secret key.
    """
    print(''.join([choice(string.ascii_letters + string.digits) for i in range(50)]))
  
