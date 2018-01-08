#!/bin/bash
# Run PetIBM

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

PETIBM_DIR="/share/data/opt/petibm/0.2"
export PATH="$PETIBM_DIR/bin:$PATH"

export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER=ofa-v2-ib0
export I_MPI_DYNAMIC_CONNECTION=0

mpirun -hosts worker4,worker5, \
	-ppn 16 \
	petibm2d \
	-log_view \
	-malloc_log \
	-memory_view \
	-options_left
