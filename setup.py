"""Standard project."""
import os
import shutil

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

if os.path.isdir(".pytest_cache") and os.path.exists(".pytest_cache"):
    print("Found $$$$ dir, cleaning...")
    shutil.rmtree(".pytest_cache")

setuptools.setup(
    name="cdk",
    version="0.1",
    description="This project is used for learning purposes",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/andrenobre88/cdk",
    packages=setuptools.find_packages(),
    author="Andre Nobre",
    author_email="andre.nobre1988@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: Public",
        "Operating System :: Serverless Application",
    ],
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=["pytest", "pylint"],
)
