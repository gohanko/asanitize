import setuptools

with open('README.md', 'r', encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='asanitize',
    version='0.0.1',
    author='Yii Kuo Chong',
    author_email='26451183+gohanko@users.noreply.github.com',
    description='A simple commandline tool to bulk delete messages/posts from your social media accounts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gohanko/asanitize',
    packages=setuptools.find_packages(include=['asanitize', 'asanitize.*']),
    install_requires=[
        'praw==7.1.0',
        'requests==2.31.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)