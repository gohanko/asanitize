# asanitize
![Status](https://github.com/gohanko/asanitize/actions/workflows/tests.yml/badge.svg)

A simple commandline tool to bulk delete messages/posts from your social media accounts. Please beware that this tool might be against TOS of some services. Use at your own risk.

## Installation
Python 3.6+ is required. For instructions on installing Python and pip see "The Hitchhiker's Guide to Python" [Installation Guides](https://docs.python-guide.org/starting/installation/)

Once installed, run the following to install `asanitize`.

```bash
pip install git+https://github.com/gohanko/asanitize
```

## Usage

### Visiting the help page
Users can visit the main and service specific help page via:
- `python -m asanitize -h`, for main page.
- `python -m asanitize <service> -h`, for service specific help page.

> NOTE: Currently supported services are `reddit` and `discord`.

### To automate tasks (for cronjobs etc.)
To automate tasks, `asanitize` supports configuration files.

Take the following step to set, and run the application with configuration files:
1. The content of the configuration file should be in `json` format. For example:
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
2. Set the configuration file location using the `--useconfig` flag. For example, `python -m asanitize <service> --useconfig <location>`.

## LICENSE
This project is license under GNU General Public License v3.0. For more information, see `LICENSE`.
