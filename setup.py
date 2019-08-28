from setuptools import setup

setup(
    name='anpr-cli',
    version='0.1',
    py_modules=['anpr'],
    install_requires=[
        'Click',
        'anprx'
    ],
    entry_points='''
        [console_scripts]
        anpr=cli.anpr:cli
    ''',
)
