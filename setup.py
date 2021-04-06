#!/usr/bin/env python
from setuptools import setup

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setup(
    name='xontrib-prompt-bar',
    version='0.3.5',
    license='BSD',
    author='anki',
    author_email='author@example.com',
    description="The bar theme for xonsh shell.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    packages=[
        'xontrib',
        'xontrib2'  # https://github.com/anki-code/xonsh-operators-proposal/blob/main/XEP-2.rst
    ],
    package_dir={'xontrib': 'xontrib', 'xontrib2': 'xontrib'},
    package_data={'xontrib': ['*.py']},
    platforms='any',
    url='https://github.com/anki-code/xontrib-prompt-bar',
    project_urls={
        "Documentation": "https://github.com/anki-code/xontrib-prompt-bar/blob/master/README.md",
        "Code": "https://github.com/anki-code/xontrib-prompt-bar",
        "Issue tracker": "https://github.com/anki-code/xontrib-prompt-bar/issues",
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Unix Shell",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: BSD License"
    ]
)
