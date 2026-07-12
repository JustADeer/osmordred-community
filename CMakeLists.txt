cmake_minimum_required(VERSION 3.28)

project(osmordred)

# Set policies
cmake_policy(SET CMP0144 NEW)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# define the C++ library "_cppmordred"
add_library(_osmordred MODULE osmordred/osmordred.cpp)

# Find and link python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
include_directories(${PYTHON_INCLUDE_DIR})

# Find and link RDKit
find_package(RDKit REQUIRED)
include_directories(${RDKit_INCLUDE_DIRS})

# Find and link Eigen
find_path(EIGEN3_INCLUDE_DIR Eigen/Dense
    PATH_SUFFIXES include/eigen3
    REQUIRED
)
include_directories(${EIGEN3_INCLUDE_DIR})

# Find Boost headers for compilation (conda version is fine for header-only features)
find_package(Boost REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
set(Boost_LIBRARIES "")

# Find and link LAPACK
find_package(LAPACK REQUIRED)
include_directories(${LAPACK_INCLUDE_DIRS})

# need explicit paths to RDKit libraries.
find_library(libRDKitDataStructs NAMES "RDKitDataStructs")
find_library(libRDKitDescriptors NAMES "RDKitDescriptors")
find_library(libRDKitFingerprints NAMES "RDKitFingerprints")
find_library(libRDKitGraphMol NAMES "RDKitGraphMol")
find_library(libRDKitPartialCharges NAMES "RDKitPartialCharges")
find_library(libRDKitRDGeneral NAMES "RDKitRDGeneral")
find_library(libRDKitSmilesParse NAMES "RDKitSmilesParse")
find_library(libRDKitSubgraphs NAMES "RDKitSubgraphs")
find_library(libRDKitSubstructMatch NAMES "RDKitSubstructMatch")

# Find pip wheel's Boost.Python to match RDKit's Boost ABI
execute_process(COMMAND ${Python3_EXECUTABLE} -c "import site; print(site.getsitepackages()[0])"
    OUTPUT_VARIABLE _site_pkg OUTPUT_STRIP_TRAILING_WHITESPACE)
file(GLOB _rdkit_boost_python "${_site_pkg}/rdkit.libs/libboost_python311-*.so*")
if(NOT _rdkit_boost_python)
    find_package(Boost REQUIRED python)
    set(_rdkit_boost_python ${Boost_PYTHON_LIBRARY})
endif()
message(STATUS "Boost.Python: ${_rdkit_boost_python}")

# Find and link RDKit libraries
target_link_libraries(_osmordred PRIVATE
    ${libRDKitDataStructs}
    ${libRDKitDescriptors}
    ${libRDKitFingerprints}
    ${libRDKitGraphMol}
    ${libRDKitPartialCharges}
    ${libRDKitRDGeneral}
    ${libRDKitSmilesParse}
    ${libRDKitSubgraphs}
    ${libRDKitSubstructMatch}
    ${LAPACK_LIBRARIES}
    ${_rdkit_boost_python}  # pip wheel's Boost.Python (matches RDKit's Boost ABI)
    ${Python3_LIBRARIES}
    )

set_target_properties(_osmordred PROPERTIES
    PREFIX ""
    SUFFIX ".so"
)

set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_INSTALL_RPATH "${Python3_LIBRARY_DIRS}")

install(TARGETS _osmordred LIBRARY DESTINATION osmordred)
