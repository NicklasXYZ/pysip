from setuptools import setup

setup(
    name = "pysip",
    url = "https://github.com/nicklasxyz/pysip",
    author = "Nicklas Sindlev Andersen",
    packages = ["pysip"],
    include_package_data = True,
    install_requires = ["jinja2", "lxml", "faker"],
    version = "0.1",
    license = "MIT",
    description = "pysip: A simple static index page generator written in python...",
    entry_points = {
        "console_scripts": [
            "pysip = pysip.src.collect:main",
        ],
    },
    long_description = open("README.md").read(),
)
