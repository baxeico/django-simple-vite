from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    README = f.read()

setup(
    name = 'django-simple-vite',
    version = '1.0.0',
    packages = find_packages(),
    author = 'Augusto Destrero',
    author_email = 'augusto@guguweb.com',
    license='MIT',
    description = 'A simple Django app to integrate Vite.js easily in your Django project.',
    long_description=README,
    long_description_content_type="text/markdown",
    url = 'https://github.com/baxeico/django-simple-vite',
    keywords = ['django', 'vitejs'],
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'Django>=3.2',
    ]
)
