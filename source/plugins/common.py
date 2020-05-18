import random, string

def random_word():
    letters = string.ascii_lowercase
    return ''.join(random.choices(letters) for i in range(24))