#!/usr/bin/env python
import git
from setuptools import setup, find_packages

def get_version():
    g = git.cmd.Git()
    version = g.describe()
    return version


if __name__ == "__main__":
    setup(
        version=get_version(),
        packages=find_packages(exclude=["*tests*"])
    )