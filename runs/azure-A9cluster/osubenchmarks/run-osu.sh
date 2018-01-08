#!/bin/bash
# Run OSU benchmark to evaluate point-to-point latency and bandwidth

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER=ofa-v2-ib0
export I_MPI_DYNAMIC_CONNECTION=0

PT2PT_DIR="/share/data/opt/osu-micro-benchmarks/5.3.2/mpi/pt2pt/"

for i in `seq 1 5`;
do
  mpirun -hosts worker0,worker1, -ppn 1 ${PT2PT_DIR}/osu_latency \
    -x 100 -i 10000 H H \
    > azurea9-latency-run$i.log

  mpirun -hosts worker0,worker1, -ppn 1 ${PT2PT_DIR}/osu_bw \
    -x 100 -i 1000 H H \
    > azurea9-bandwidth-run$i.log
done
