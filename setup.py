import os
import sys
from skbuild import setup

prefix = os.environ.get("CONDA_PREFIX") or getattr(sys, "prefix", None)
cmake_args = []
if prefix:
    cmake_args.append(f"-DCMAKE_PREFIX_PATH={prefix}")

setup(
    packages=["osmordred"],
    cmake_args=cmake_args,
)
