from setuptools import setup

setup(
    name='anpr-cli',
    version='0.1',
    url="https://github.com/ppintosilva/anpr-cli",
    author_email="ppintodasilva@gmail.com",
    py_modules=[],
    install_requires=[
        'Click',
        'anprx >= 0.1.3'
    ],
    entry_points='''
        [console_scripts]
        anpr=cli.anpr:cli
    ''',
    dependency_links = ['http://github.com/ppintosilva/anpr-cli/tarball/v0.1.3#egg=package-1.0']
)
