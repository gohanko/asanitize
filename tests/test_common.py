from asanitize.common import random_word

def test_random_word():
    words = random_word()
    assert len(words) == 2000
