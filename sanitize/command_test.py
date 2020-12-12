from cleo import Application
from sanitize.command import create_cleo_app

def test_create_cleo_app():
    cleo_app = create_cleo_app()
    assert isinstance(cleo_app, Application) == True