from os.path import join
from setuptools import setup, find_packages


long_description = (
    open('README.rst').read() + open('CHANGES.rst').read())


def get_version():
    with open(join('transaction_hooks', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')


setup(
    name='django-transaction-hooks',
    version=get_version(),
    description=(
        'Django database backends that permit registering '
        'post-transaction-commit hooks'
        ),
    long_description=long_description,
    author='Carl Meyer',
    author_email='carl@oddbird.net',
    url='https://github.com/carljm/django-transaction-hooks/',
    packages=find_packages(),
    install_requires=['django>=1.6.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
    ],
    zip_safe=False,
)
