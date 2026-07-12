# Osmordred-Community

A community maintained version of [_Osmordred_](https://github.com/osmoai/osmordred) which is no longer maintained.

Osmordred was inspired by the Dragon, Padel, Mordred and other toolkits to generate empirical molecular features.
Our goal focuses only on 0D, 1D and 2D molecular descriptors fused with RDKit backend at C++ level to get very fast computation in parallel if needed.

## Remark on reproducibility

I spent quite some time to implement a decent Information Content descriptor version based on the first paper from 1984 where Basak describes in detail his method https://doi.org/10.1016/B978-0-08-030156-3.50138-7.
So our implementation of Information Content is not 100% identical to Basak, Padel and Mordred but it follows the core Basak logic within RDKit where aromaticity is "specific".
This was indeed during this period that I also implemented the Triplet features from Basak team.

## Future
Current version is around 10k lines of codes in only one file. 
It will be great to better integrate and refactor python bindings.
Additionally a list of other descriptors were added to produce now 3586 individual features.

## Speed
This is fully parallelized. LAPACK was selected for its speed especially on the SVD decomposition of symmetric squared matrix instead of Eigen3 solvers.
LAPACK can produce very small fluctuation for almost-zero eigenvalues and affects very slightly few descriptors.

## Installation

Requires Python 3.11+ with a conda environment.

### Method 1: from scratch
```
./setup_env.sh
conda activate osmordred-community
pip install -v .
```

### Method 2: into your current environment
```
conda install -y boost eigen lapack ninja rdkit scikit-build numpy -c conda-forge
source scripts/provision_rdkit_headers.sh
pip install -v .
```

### Verify
```
python -c "import osmordred; print('OK')"
python -c "
from rdkit import Chem
import osmordred
mol = Chem.MolFromSmiles('c1ccccc1')
print('MW:', list(osmordred.CalcWeight(mol)))
```

> **Note:** `import osmordred` from the repo root imports the local `osmordred/` directory (missing the compiled C extension), not the installed package. Run Python from another directory, or `cd /tmp && python ...`.

### Run tests
```
pip install tqdm
python tests/tAll.py
```

### Known issue
Complex molecules can cause slow computation due to intensive descriptor evaluation:
```
c12c3c4c5c1c1c6c7c2c2c8c3c3c9c4c4c%10c5c5c1c1c6c6c%11c7c2c2c7c8c3c3c8c9c4c4c9c%10c5c5c1c1c6c6c%11c2c2c7c3c3c8c4c4c9c5c1c1c6c2c3c41
```

## License

[BSD-3-Clause](license.txt)
