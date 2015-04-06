from setuptools import setup, find_packages
import sys

setup(
    name="arrow_of_time",
    version="0.0.1-dev",
    packages=find_packages(),

    # Metadata for PyPi
    author="Jonathan Heathcote",
    description="A universe model to demonstrate the arrow of time.",
    license="GPLv2",

    # Requirements
    install_requires=[],
    tests_require=["pytest>=2.6"],
)
