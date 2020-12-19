import setuptools

with open('docs/README.md', 'r', encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='asanitize',
    version='0.0.5',
    author='Brandon',
    author_email='pleasecontactmeongithub@localhost.local',
    description='A simple commandline tool to bulk delete messages/posts from your social media accounts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gohanko/asanitize',
    packages=setuptools.find_packages(include=['asanitize']),
    install_requires=[
        'praw==7.1.0',
        'PyYAML==5.3.1',
        'requests==2.25.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
