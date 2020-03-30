"""Setup script."""

from setuptools import setup, find_packages

setup(
    name="raspylogger",
    version="0.1.0",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[],
    packages=find_packages(),
)
