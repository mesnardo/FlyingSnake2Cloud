#!/bin/bash
# Get, configure and build PETSc-3.7.4 in production mode

PETSC_VERSION="3.7.4"
PETSC_DIR="/share/data/opt/petsc/${PETSC_VERSION}"
mkdir -p ${PETSC_DIR}

cd /tmp
TARBALL="petsc-lite-${PETSC_VERSION}.tar.gz"
wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/${TARBALL}
tar -xzf ${TARBALL} -C ${PETSC_DIR} --strip-components=1

yum -y install bison flex cmake gcc-gfortran

source /opt/intel2/bin/compilervars.sh -arch intel64 -platform linux
source /opt/intel2/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

cd ${PETSC_DIR}
PETSC_ARCH="linux-opt"
./configure --PETSC_DIR=${PETSC_DIR} --PETSC_ARCH=${PETSC_ARCH} \
  --with-mpi-dir="/opt/intel2/compilers_and_libraries/linux/mpi/intel64" \
  --COPTFLAGS="-O3" \
  --CXXOPTFLAGS="-O3" \
  --FOPTFLAGS="-O3" \
  --with-debugging=0 \
  --download-fblaslapack \
  --download-hypre \
  --download-hdf5 \
  --download-ptscotch \
  --download-metis \
  --download-parmetis \
  --download-superlu_dist

make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} all
make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} test

rm -f /tmp/${TARBALL}
