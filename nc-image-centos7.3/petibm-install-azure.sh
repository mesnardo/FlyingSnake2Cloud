#!/bin/bash
# Installation script for PetIBM.


# Set sudo mode.
sudo -s

# Install prerequisites.
# yum install -y libmlx4 librdmacm libibverbs dapl rdma
yum install -y wget git gcc gcc-c++ gcc-gfortran make cmake flex bison

# Install Intel MPI Library
cd /tmp
tar -xzf l_mpi_2017.2.174.tgz
cd l_mpi_2017.2.174
sed -i -e 's/^ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' silent.cfg
sed -i -e 's/^ARCH_SELECTED=ALL/ARCH_SELECTED=INTEL64/g' silent.cfg
./install.sh -s silent.cfg
cd ..
rm -rf l_mpi_2017.2.174 l_mpi_2017.2.174.tgz
tar -xzf l_mkl_2017.2.174.tgz
cd l_mkl_2017.2.174
sed -i -e 's/^ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' silent.cfg
sed -i -e 's/^ARCH_SELECTED=ALL/ARCH_SELECTED=INTEL64/g' silent.cfg
./install.sh -s silent.cfg
cd ..
rm -rf l_mkl_2017.2.174 l_mkl_2017.2.174.tgz

# Add MPI wrappers to the PATH environment variable.
source /opt/intel/bin/compilervars.sh -arch intel64 -platform linux
source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

# Install PETSc-3.7.4.
PETSC_VERSION=3.7.4
PETSC_TARBALL=petsc-lite-${PETSC_VERSION}.tar.gz
wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/${PETSC_TARBALL} -P /tmp
PETSC_DIR=/opt/petsc/${PETSC_VERSION}
PETSC_ARCH=linux-gnu-intel-opt
mkdir -p ${PETSC_DIR}
tar -xzf /tmp/${PETSC_TARBALL} -C ${PETSC_DIR} --strip-components=1
cd ${PETSC_DIR}
./configure \
  --PETSC_DIR=${PETSC_DIR} \
  --PETSC_ARCH=${PETSC_ARCH} \
  --with-cc=mpicc \
  --with-cxx=mpicxx \
  --with-fc=mpif90 \
  --COPTFLAGS=-O3 \
  --CXXFLAGS=-O3 \
  --FOPTFLAGS=-O3 \
  --with-debugging=0 \
  --with-blas-lapack-dir=/opt/intel/mkl \
  --download-hypre \
  --download-hdf5 \
  --download-ptscotch \
  --download-metis \
  --download-parmetis \
  --download-superlu_dist
make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} all
make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} test
rm -f /tmp/${PETSC_TARBALL}

# Install CUDA Toolkit 8.0.
cd /tmp
yum install -y kernel-devel
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install -y dkms
CUDA_REPO_PKG=cuda-repo-rhel7-8.0.61-1.x86_64.rpm
wget http://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/${CUDA_REPO_PKG} -O /tmp/${CUDA_REPO_PKG}
rpm -ivh /tmp/${CUDA_REPO_PKG}
rm -f /tmp/${CUDA_REPO_PKG}
yum install -y cuda-drivers cuda
CUDA_DIR=/usr/local/cuda-8.0
export PATH=${CUDA_DIR}/bin:$PATH
export LD_LIBRARY_PATH=${CUDA_DIR}/lib64:$LD_LIBRARY_PATH

# Install AmgX-2.0
AMGX_VERSION=2.0
AMGX_TARBALL=amgx-2.0-src.tar
AMGX_DIR=/opt/amgx/${AMGX_VERSION}
AMGX_BUILD=${AMGX_DIR}/build
mkdir -p ${AMGX_DIR} ${AMGX_BUILD}
tar -xzf /tmp/${AMGX_TARBALL} -C ${AMGX_DIR}
cd ${AMGX_BUILD}
cmake ${AMGX_DIR}
make -j"$(nproc)" all
make install
rm -f /tmp/${AMGX_TARBALL} /opt/amgx/srcTarball.txt

# Install PetIBM.
PETIBM_DIR=/opt/petibm
git clone https://github.com/mesnardo/PetIBM.git ${PETIBM_DIR}
cd ${PETIBM_DIR}
git checkout -b master-noversionchecks origin/master-noversionchecks
PETIBM_BUILD=${PETIBM_DIR}/build
mkdir -p ${PETIBM_BUILD}
cd ${PETIBM_BUILD}
${PETIBM_DIR}/configure --prefix=/usr/local \
  CXX=mpicxx \
  CXXFLAGS="-O3 -w -std=c++11" \
  --with-petsc-dir=${PETSC_DIR} \
  --with-petsc-arch=${PETSC_ARCH} \
  --with-cuda=${CUDA_DIR} \
  --with-amgx=${AMGX_DIR}
make -j"$(nproc)" all
make check
make install
