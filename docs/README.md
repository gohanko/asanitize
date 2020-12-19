# asanitize
A simple commandline tool to bulk delete messages/posts from your social media accounts. Please beware that using this tool on some services such as Discord is against their TOS and you might get banned.

## Installation (not available yet, under work)
`asanitize` is supported on Python 3.6+. The recommended way to install `asanitize` is via [pip](https://pypi.org/project/pip/)

```bash
pip install asanitize
```

For instructions on installing Python and pip see "The Hitchhiker's Guide to Python" [Installation Guides](https://docs.python-guide.org/starting/installation/)

You can also install this manually using commandline by

1. Cloning the asanitize project into a directory.
2. Change directory into the project directory and install the dependencies via `pip install -r requirements.txt`.
3. Run `python setup.py install` to install the package and the `asanitize` commandline utility. Congratulations, you can now use it anywhere by invoking `python -m asanitize`.
4. Another way to use it is, from the root of the project directory run `python -m asanitize`, however you have to go into the project directory everytime you want to use it. 

## Usage
After installing the software, you can visit the help page via `python -m asanitize -h` for help on how to use it. 

Please keep in mind that every service has its own help page as well, running `python -m asanitize discord -h` will show you the help page for the discord sanitizer while running `python -m asanitize reddit -h` will show you the help page for the reddit sanitizer.

The currently supported services are `discord`, and `reddit`. There are plans to add `twitter` and `telegram` as well but I haven't gotten around to doing that.

> NOTE: A "service/services" is the name used to describe what service you want to sanitize, e.g `discord` is for the Discord messaging system, and `reddit` is for the Reddit social media platform.

### Configuration Files
For users who wants to automate the task, `asanitize` also allows for the use of configuration files. This will allow users to set authentication tokens as well as different behaviours without typing it out everytime.

You can tell `asanitize` which file to look at by using the `--file` flag after selecting which service you want to use, e.g `python -m sanitize <discord|reddit> --file /home/nobody/env.yml`.

For an example of how a configuration file should look like, please have a look at [example.env.yml](./example.env.yml).

## Contributions
Whether it's fixing typos, writing documentations or pushing code, anyone is welcomed to contribute. Please have a look at the issues board things to do.

Other than that, if you cannot find any or is still lost you can help with these:

- Writing a guide on how to get discord authentication tokens.
- Writing a guide on how to get reddit authentication details.
- Writing tests (I'm having a hard time writing tests for code that interacts with 3rd party systems, stubbing api calls seems to be too much hassle and testing it directly seems to depend on 3rd party too much).

## LICENSE
This project is license under GNU General Public License v3.0. For more information, see `LICENSE`.
