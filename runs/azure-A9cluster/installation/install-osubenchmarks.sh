#!/bin/bash
# Install OSU micro benchmarks

cd /tmp
OSU_VERSION="5.3.2"
TARBALL="osu-micro-benchmarks-${OSU_VERSION}.tar.gz"
wget http://mvapich.cse.ohio-state.edu/download/mvapich/${TARBALL}
OSU_DIR=/share/data/opt/osu-micro-benchmarks/${OSU_VERSION}
mkdir -p ${OSU_DIR}
tar -xzf ${TARBALL} -C ${OSU_DIR} --strip-components=1

source /opt/intel2/bin/compilervars.sh -arch intel64 -platform linux
source /opt/intel2/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

cd ${OSU_DIR}
./configure --prefix=${OSU_DIR} \
	CC=mpicc \
	CXX=mpicxx
make -j "$(nproc)" install

rm -f /tmp/${TARBALL}
