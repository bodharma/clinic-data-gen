from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Test Data generation tool"


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clinical-data-gen",
    version=VERSION,
    author="bohdan-lesiv",
    author_email="bohdan.lesiv@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.9",
    install_requires=["protobuf"],
)
