# asanitize
![Status](https://github.com/gohanko/asanitize/actions/workflows/tests.yml/badge.svg)

A simple commandline tool to bulk delete messages/posts from your social media accounts. Please beware that using this tool on some services such as Discord is against their TOS and you might get banned.

## Installation
Python 3.6+ is required. For instructions on installing Python and pip see "The Hitchhiker's Guide to Python" [Installation Guides](https://docs.python-guide.org/starting/installation/)

Once you have Python installed, you can run the following to install `asanitize`.

```bash
pip install git+https://github.com/gohanko/asanitize
```

## Usage
After installing the software, you can visit the help page via `python -m asanitize -h` for help on how to use it. Every service has its own help page as well, you can check them by running `python -m asanitize <service> -h`. Currently supported services are `reddit` and `discord`.

### Configuration Files
For users who wants to automate the task, `asanitize` also allows for the use of configuration files. This will allow users to set authentication tokens as well as different behaviours without typing it out everytime.

You can tell `asanitize` which file to look at by using the `--useconfig` flag after selecting which service you want to use. For example, `python -m asanitize <service> --useconfig <location>`.

Config example:
```json
{
    "discord": {
        "token": "",
        "channels_to_sanitize": [],
        "fastmode": false
    },
    "reddit": {
        "client_id": "",
        "client_secret": "",
        "username": "",
        "password": ""
    }
}
```

## LICENSE
This project is license under GNU General Public License v3.0. For more information, see `LICENSE`.
