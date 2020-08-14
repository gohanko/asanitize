"""
    common.py - Common functions

    Contains common functions shared 
    between our plugins.
"""

import random
import string

def random_word():
    """Generates a random word at the length of 2000 characters"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(2000))
