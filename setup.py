from setuptools import setup, find_packages

setup(
    name='remote_shell',
    version='0.1.0',
    packages=find_packages(include=[
        'remote_shell', 'remote_shell.*',
        'modules', 'modules.*',
    ]),
    install_requires=[
        'pynput',
        'sounddevice',
        'wavio',
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'rclient=remote_shell.main:main',
            'rserver=remote_shell.server:main',
        ],
    },
)

