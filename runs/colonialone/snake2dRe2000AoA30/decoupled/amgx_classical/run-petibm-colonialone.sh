#!/bin/sh

#SBATCH --job-name="LIamgxcla"
#SBATCH --output=log%j.out
#SBATCH --error=log%j.err
#SBATCH --partition=ivygpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --time=48:00:00

module load gcc/4.9.2
module load openmpi/1.8/gcc/4.9.2
module load cuda/toolkit/6.5

PETIBM_DIR="$HOME/src/petibm/0.2"
export PATH="$PETIBM_DIR/bin:$PATH"

AMGX_DIR="$HOME/src/amgx"
export LD_LIBRARY_PATH="$AMGX_DIR/lib:$LD_LIBRARY_PATH"
export LM_LICENSE_FILE="$AMGX_DIR/amgx_trial.lic"

export CUDA_VISIBLE_DEVICES=0,1

mpiexec -display-map petibm2d \
	-log_view \
	-malloc_log \
	-memory_view \
	-options_left
