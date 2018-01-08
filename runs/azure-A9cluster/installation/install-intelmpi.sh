#!/bin/bash
# Install Intel MPI library

cd /tmp
MPI_FOLDER="l_mpi_2017.2.174"
TARBALL="${MPI_FOLDER}.tgz"
tar -xzf ${TARBALL}
cd ${MPI_FOLDER}
CONFIG_FILE="/tmp/silent.cfg"
./install.sh --silent ${CONFIG_FILE}
rm -rf /tmp/${MPI_FOLDER} ${CONFIG_FILE}
