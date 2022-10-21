from setuptools import setup, find_packages 
from objectid import VERSION

with open("readme.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name = 'django-objectid',
    version = VERSION,
    description = 'django objectid',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/tangdyy/django-objectid",
    author = 'Tang dayong', 
    author_email = "tangdyy@126.com",
    install_requires = [
        'django>=2.2.0',
        'psutil>=5.9.2'
    ],
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6' 
)