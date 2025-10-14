from setuptools import setup, find_packages

setup(
    name="telem-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click", "requests"],
    entry_points={
        "console_scripts": [
            "telem=telem_cli.cli:cli"
        ]
    },
)
