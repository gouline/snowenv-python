#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    raise ValueError("Requires Python 3.6+")


def requires_from_file(filename: str) -> list:
    with open(filename, "r") as f:
        return [x.strip() for x in f if x.strip()]


with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name="snowenv",
    use_scm_version=True,
    description="Environment switching for Snowflake Connector for Python",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://github.com/gouline/snowenv-python",
    packages=find_packages(exclude=["tests"]),
    test_suite="tests",
    install_requires=requires_from_file("requirements.txt"),
    extras_require={
        "test": requires_from_file("requirements-test.txt"),
    },
    setup_requires=["setuptools_scm"],
)
