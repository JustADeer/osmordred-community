#!/bin/bash
set -e

function print_error {
    echo
    echo "Failed to create conda environment!!"
    exit 1
}
trap print_error ERR

echo "Removing existing environment (if present)"
conda env remove -y -n osmordred-community &>/dev/null || true

conda_packages="boost eigen lapack ninja rdkit"
if [[ "$OSTYPE" =~ ^darwin.* ]]; then
    echo "Creating conda env with MacOS packages"
    conda_packages="$conda_packages blas=*=*openblas"
elif [[ "$OSTYPE" =~ ^linux.* ]]; then
    echo "Creating conda env with Linux packages"
    conda_packages="$conda_packages blas=*=*mkl"
else
    echo "Don't recogize os: $OSTYPE"
    exit 1
fi

conda create -y -n osmordred-community $conda_packages python=3.11 -c conda-forge

eval "$(conda shell.bash hook)"
conda activate osmordred-community
source "$(dirname "$0")/scripts/provision_rdkit_headers.sh"
