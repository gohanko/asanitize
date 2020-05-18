import random, string

def random_word():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(24))