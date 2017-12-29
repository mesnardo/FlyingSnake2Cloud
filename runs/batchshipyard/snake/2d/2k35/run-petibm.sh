#!/bin/bash

SIMULATION_DIR=$1

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

# get number of GPUs on machine
ngpus=`nvidia-smi -L | wc -l`
echo "num gpus: $ngpus"

# get number of nodes
IFS=',' read -ra HOSTS <<< "$AZ_BATCH_HOST_LIST"
nodes=${#HOSTS[@]}

# number of processes per node
n=12
# number of processes
np=$(($nodes * $n))

echo "num nodes: $nodes"
echo "hosts: $AZ_BATCH_HOST_LIST"
echo "num processes per node: $n"
echo "PATH: $PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

mpirun -np $np -ppn $n -host $AZ_BATCH_HOST_LIST \
  -env I_MPI_FABRICS=shm:dapl \
  -env I_MPI_DAPL_PROVIDER=ofa-v2-ib0 \
  -env I_MPI_DYNAMIC_CONNECTION=0 \
  -env CUDA_VISIBLE_DEVICES=0,1 \
  petibm2d \
  -directory $SIMULATION_DIR \
  -log_view \
  -malloc_log \
  -memory_view \
  -options_left

