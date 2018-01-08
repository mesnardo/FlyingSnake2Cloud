#!/bin/sh

#SBATCH --job-name="7nodes"
#SBATCH --output=poisson-hypre-7nodes.out
#SBATCH --error=poisson-hypre-7nodes.err
#SBATCH --partition=defq
#SBATCH --nodes=7
#SBATCH --ntasks-per-node=16
#SBATCH --time=00:30:00

module load gcc/4.9.2
module load openmpi/1.8/gcc/4.9.2
module load cuda/toolkit/6.5

export LD_LIBRARY_PATH="$HOME/src/amgx/lib:$LD_LIBRARY_PATH"
export LM_LICENSE_FILE="$HOME/src/amgx/amgx_trial.lic"

AMGXWRAPPER_EXAMPLE="$HOME/src/amgxwrapper/1.0-beta2/example/Poisson"
export PATH="$AMGXWRAPPER_EXAMPLE/bin:$PATH"

export CUDA_VISIBLE_DEVICES=0,1

CFG_FILE="configPETScHypre.info"

mpiexec -display-map Poisson \
  -caseName test \
  -mode PETSc \
  -Nx 1070 -Ny 1070 -Nz 40 \
  -cfgFileName $CFG_FILE \
  -optFileName poisson-hypre-7nodes
