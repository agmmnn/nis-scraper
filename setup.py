from setuptools import setup, find_packages
import nisanyan_crawler

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as file:
    requires = [line.strip() for line in file.readlines()]

VERSION = "0.0.2"
DESCRIPTION = (
    "Crawler for the online Turkish etymological dictionary, nisanyansozluk.com."
)

setup(
    name="nisanyan_crawler",
    version=VERSION,
    url="https://github.com/agmmnn/nisanyan_crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="agmmnn",
    license="Apache License Version 2.0",
    license_files=["LICENSE"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    packages=["nisanyan_crawler"],
    install_requires=requires,
    include_package_data=True,
    package_data={"nisanyan_crawler": ["nisanyan_crawler/*"]},
    python_requires=">=3.5",
    entry_points={
        "console_scripts": ["nisanyan_crawler = nisanyan_crawler.__main__:cli"]
    },
)
