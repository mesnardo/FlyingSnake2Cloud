#!/usr/bin/env bash
# Computes the x- and z-components of the 3D vorticity field.
# CLI: ./compute-wx-wz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)

source $(dirname $SIMU_DIR)/bashrc

# Set the main directory of the data.
DATA_DIR=$SIMU_DIR
# Set the output directory.
OUT_DIR="$SIMU_DIR/postprocessing/vorticity"

np=4

echo "Computing wx and wz ..."
mpiexec -np $np petibm-vorticity3d \
	-data_directory $DATA_DIR \
	-output_directory $OUT_DIR \
	-grid_directory $DATA_DIR/grids \
	-nstart 5000 -nend 100000 -nstep 5000 \
	-nx 1071 -ny 1072 -nz 40 \
	-periodic_z \
	-compute_wx -compute_wz
