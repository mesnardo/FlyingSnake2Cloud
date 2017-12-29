#!/bin/bash
# Run OSU benchmark to evaluate point-to-point latency and bandwidth

OUTPUT_DIR=$1

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

PT2PT_DIR="/opt/osu-micro-benchmarks/5.3.2/mpi/pt2pt"
export PATH=${PT2PT_DIR}:${PATH}

for i in `seq 1 5`; do
    mpirun -n 2 --ppn 1 --host $AZ_BATCH_HOST_LIST \
        -env I_MPI_FABRICS=tcp \
        -env I_MPI_DYNAMIC_CONNECTION=0 \
        osu_latency \
        -x 100 -i 10000 H H \
        > ${OUTPUT_DIR}/nc24r-latency-run$i.log

    mpirun -n 2 --ppn 1 --host $AZ_BATCH_HOST_LIST \
        -env I_MPI_FABRICS=tcp \
        -env I_MPI_DYNAMIC_CONNECTION=0 \
        osu_bw \
        -x 100 -i 1000 H H \
        > ${OUTPUT_DIR}/nc24r-bandwidth-run$i.log
done
