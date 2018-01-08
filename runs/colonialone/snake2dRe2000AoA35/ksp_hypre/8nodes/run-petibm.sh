#!/bin/sh

#SBATCH --job-name="hypn8"
#SBATCH --output=log%j.out
#SBATCH --error=log%j.err
#SBATCH --partition=defq
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=16
#SBATCH --time=12:00:00


module load gcc/4.9.2
module load openmpi/1.8/gcc/4.9.2
module load cuda/toolkit/6.5

PETIBM_DIR="$HOME/src/petibm/0.2"
export PATH="$PETIBM_DIR/bin:$PATH"

mpiexec -display-map petibm2d \
	-log_view \
	-malloc_log \
	-memory_view \
	-options_left
