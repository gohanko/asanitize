from sanitize.common import random_word, load_config_from_file

def test_random_word():
    words = random_word()
    assert len(words) == 2000

def test_load_config_from_file():
    config = load_config_from_file('./example.env.yml', 'discord')

    assert isinstance(config, object) == True
    assert config['token'] == 'invalid_token'
