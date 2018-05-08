#!/usr/bin/env bash
# Computes the x- and z-components of the 3D vorticity field.
# CLI: ./compute-wx-wz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Set the main directory of the data.
DATA_DIR="$SIMU_DIR/postprocessing/solution-crop"
# Set the output directory.
OUT_DIR="$SIMU_DIR/postprocessing/vorticity-crop"

np=4

echo "Computing wx and wz ..."
mpiexec -np $np petibm-vorticity3d \
	-data_directory $DATA_DIR \
	-output_directory $OUT_DIR \
	-grid_directory $DATA_DIR/grids \
	-nstart 100000 -nend 200000 -nstep 2000 \
	-nx 690 -ny 500 -nz 40 \
	-periodic_z \
	-compute_wx -compute_wz
