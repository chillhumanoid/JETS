from setuptools import setup, find_packages

setup(
    name='JETS',
    version='2.0',
    py_modules=['jets'],
    install_requires=[
        'Click',
        'PyPDF2',
        'configparser',
        'pathvalidate',
        'requests',
        'bs4',
    ],
    entry_points='''
        [console_scripts]
        jets=jets:cli
    ''',
)
