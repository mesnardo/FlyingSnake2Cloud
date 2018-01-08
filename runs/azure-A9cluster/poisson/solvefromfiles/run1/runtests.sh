#!/bin/bash

AMGXWRAPPER_DIR="${HOME}/AmgXWrapper"
AMGXWRAPPER_EXAMPLE="${AMGXWRAPPER_DIR}/example/solveFromFiles"
export PATH="${AMGXWRAPPER_EXAMPLE}/bin:${PATH}"

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER=ofa-v2-ib0
export I_MPI_DYNAMIC_CONNECTION=0

CFG_FILE="testcase/solversPetscOptions-test.info"

mpirun -hosts worker0,worker1,worker2,worker3,worker4,worker5,worker6,worker7, -ppn 16 \
	solveFromFiles \
	-caseName test \
	-mode PETSc \
	-cfgFileName ${CFG_FILE} \
	-matrixFileName testcase/QTBNQ.mtx \
	-rhsFileName testcase/rhs2.vec \
	-optFileName performance-8nodes
