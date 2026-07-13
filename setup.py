import os
import sys
from skbuild import setup
from setuptools import find_packages

prefix = os.environ.get("CONDA_PREFIX") or getattr(sys, "prefix", None)
cmake_args = []
if prefix:
    cmake_args.append(f"-DCMAKE_PREFIX_PATH={prefix}")

setup(
    name="osmordred",
    version="0.1.0",
    description="osmordred-community",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy",
        "rdkit",
    ],
    cmake_args=cmake_args,
)