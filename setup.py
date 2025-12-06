"""Setup configuration for sentence-autocomplete package."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sentence-autocomplete",
    version="1.0.0",
    author="Susheel-1999",
    description="A sentence autocompletion system using pre-trained language models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Susheel-1999/sentence-autocomplete",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "transformers>=4.48.0",
        "torch>=2.6.0",
    ],
    entry_points={
        "console_scripts": [
            "sentence-autocomplete=src.cli:main",
        ],
    },
)
