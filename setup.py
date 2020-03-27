from setuptools import setup, find_packages
from os.path import join, dirname
import manybots

setup(
    name='manybots',
    version=manybots.__version__,
    author='Senderman',
    author_email='doletov.fyodor@yandex.ru',
    description='Lib for running multiple pyTelegramBotAPI instances using threading',
    long_description=open(join(dirname(__file__), 'README.md'), encoding='utf-8').read(),
    url='https://github.com/Senderman/manybotslib',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
