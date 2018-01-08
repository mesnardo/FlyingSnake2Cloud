#!/bin/bash
# Configures, builds, and installs PetIBM-0.2 in production mode

PETIBM_VERSION="0.2"
PETIBM_DIR="/share/data/opt/petibm/${PETIBM_VERSION}"
mkdir -p ${PETIBM_DIR}

cd /tmp
TARBALL="v${PETIBM_VERSION}.tar.gz"
wget https://github.com/barbagroup/PetIBM/archive/${TARBALL}
tar -xzf ${TARBALL} -C ${PETIBM_DIR} --strip-components=1

source /opt/intel2/bin/compilervars.sh -arch intel64 -platform linux
source /opt/intel2/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

PETSC_DIR="/share/data/opt/petsc/3.7.4"
PETSC_ARCH="linux-opt"

cd ${PETIBM_DIR}
./configure --prefix=${PETIBM_DIR} \
        CXX=mpicxx \
        CXXFLAGS="-O3 -w -std=c++0x" \
        --with-petsc-dir=${PETSC_DIR} \
        --with-petsc-arch=${PETSC_ARCH}

make all
make install

rm -f /tmp/${TARBALL}
