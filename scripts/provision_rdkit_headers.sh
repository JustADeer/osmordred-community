#!/bin/bash
set -e

RDKIT_INCLUDE="$CONDA_PREFIX/include/rdkit"

already_provisioned() {
    [ -f "$RDKIT_INCLUDE/GraphMol/ROMol.h" ]
}

if already_provisioned; then
    echo "RDKit C++ headers already provisioned at $RDKIT_INCLUDE"
    return 0 2>/dev/null || exit 0
fi

echo "Provisioning RDKit C++ headers..."

RDKIT_VER=$(python -c "import rdkit; print(rdkit.__version__)")
RDKIT_TAG="Release_${RDKIT_VER//./_}"

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

curl -sL "https://github.com/rdkit/rdkit/archive/refs/tags/${RDKIT_TAG}.tar.gz" | tar xz -C "$TMPDIR"
SRCDIR="$TMPDIR/rdkit-${RDKIT_TAG}"

mkdir -p "$TMPDIR/build" && cd "$TMPDIR/build"
cmake "$SRCDIR" -DRDK_BUILD_PYTHON_WRAPPERS=OFF -DRDK_BUILD_CPP_TESTS=OFF \
    -DCMAKE_INSTALL_PREFIX="$CONDA_PREFIX" -DCMAKE_PREFIX_PATH="$CONDA_PREFIX" \
    -DRDK_INSTALL_INTREE=OFF > /dev/null 2>&1
cmake --build . --target RDGeneral > /dev/null 2>&1 || true

mkdir -p "$RDKIT_INCLUDE"
for dir in "$SRCDIR"/Code/*/; do
    name=$(basename "$dir")
    mkdir -p "$RDKIT_INCLUDE/$name"
    find "$dir" -maxdepth 1 -name "*.h" -exec cp {} "$RDKIT_INCLUDE/$name/" \; 2>/dev/null || true
done
for subdir in $(find "$SRCDIR/Code" -type d); do
    rel="${subdir#$SRCDIR/Code/}"
    [ -z "$rel" ] && continue
    mkdir -p "$RDKIT_INCLUDE/$rel"
    find "$subdir" -maxdepth 1 -name "*.h" -exec cp {} "$RDKIT_INCLUDE/$rel/" \; 2>/dev/null || true
done

cp "$TMPDIR/build/Code/RDGeneral/export.h.tmp" "$RDKIT_INCLUDE/RDGeneral/export.h"
cp "$SRCDIR/Code/RDGeneral/RDExportMacros.h" "$RDKIT_INCLUDE/RDGeneral/"

cat > "$RDKIT_INCLUDE/RDGeneral/RDConfig.h" << 'RDCEOF'
#define RDK_USE_BOOST_SERIALIZATION
#define RDK_USE_BOOST_IOSTREAMS
#define RDK_OPTIMIZE_POPCNT
#define RDK_BUILD_THREADSAFE_SSS
#define RDK_USE_STRICT_ROTOR_DEFINITION
#define RDK_BUILD_DESCRIPTORS3D
#define RDK_HAS_EIGEN3
#define RDK_BUILD_COORDGEN_SUPPORT
#define RDK_BUILD_MAEPARSER_SUPPORT
#define RDK_BUILD_AVALON_SUPPORT
#define RDK_BUILD_INCHI_SUPPORT
#define RDK_BUILD_SLN_SUPPORT
#define RDK_BUILD_CAIRO_SUPPORT
#define RDK_BUILD_FREETYPE_SUPPORT
#define RDK_USE_URF
#define RDK_BUILD_YAEHMOP_SUPPORT
RDCEOF

echo "RDKit C++ headers provisioned at $RDKIT_INCLUDE"
