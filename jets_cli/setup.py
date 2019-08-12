from setuptools import setup

setup(
    name='JETS',
    version='1.0',
    py_modules=['jets'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        jets=jets:cli
        hello=jets:hello
    ''',
)
