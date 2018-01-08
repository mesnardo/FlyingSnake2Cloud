#!/bin/bash

AMGXWRAPPER_DIR="${HOME}/AmgXWrapper"
AMGXWRAPPER_POISSON="${AMGXWRAPPER_DIR}/example/Poisson"
export PATH="${AMGXWRAPPER_POISSON}/bin:${PATH}"

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER=ofa-v2-ib0
export I_MPI_DYNAMIC_CONNECTION=0

CFG_FILE="configPETScHypre.info"

for i in `seq 1 5`;
do
	mkdir run$i
	cp ${CFG_FILE} run$i
	cd run$i
	mpirun -hosts worker0, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-1node > output-1node.txt

	mpirun -hosts worker0,worker1, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-2nodes > output-2nodes.txt
	mpirun -hosts worker0,worker1,worker2, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-3nodes > output-3nodes.txt
	mpirun -hosts worker0,worker1,worker2,worker3, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-4nodes > output-4nodes.txt
	mpirun -hosts worker0,worker1,worker2,worker3,worker4, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-5nodes > output-5nodes.txt
	mpirun -hosts worker0,worker1,worker2,worker3,worker4,worker5, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-6nodes > output-6nodes.txt
	mpirun -hosts worker0,worker1,worker2,worker3,worker4,worker5,worker6, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-7nodes > output-7nodes.txt
	mpirun -hosts worker0,worker1,worker2,worker3,worker4,worker5,worker6,worker7, \
		-ppn 16 \
		Poisson \
		-caseName test \
		-mode PETSc \
		-Nx 1070 -Ny 1070 -Nz 40 \
		-cfgFileName ${CFG_FILE} \
		-optFileName performance-8nodes > output-8nodes.txt
	cd ..
done
