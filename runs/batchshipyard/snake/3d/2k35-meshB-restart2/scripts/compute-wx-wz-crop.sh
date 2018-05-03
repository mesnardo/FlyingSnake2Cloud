#!/usr/bin/env bash
# Computes the x- and z-components of the 3D vorticity field.
# CLI: ./compute-wx-wz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)

source $(dirname $SIMU_DIR)/bashrc

# Set the directory that contains the data.
DATA_DIR="$SIMU_DIR/postprocessing/solution-crop"
# Set the output directory.
OUT_DIR="$SIMU_DIR/postprocessing/vorticity-crop"

# Set the common command-line arguments.
common_args="
-data_directory $DATA_DIR \
-output_directory $OUT_DIR \
-grid_directory $DATA_DIR/grids \
-nstart 249600 -nend 281600 -nstep 3200 \
-nx 1279 -ny 1000 -nz 80 \
-periodic_z
"
np=6

# Compute the x-component of the vorticity field.
echo "Computing wx ..."
mpiexec -np $np petibm-vorticity3d \
	-compute_wx \
	$common_args
# Compute the z-component of the vorticity field.
echo "Computing wz ..."
mpiexec -np $np petibm-vorticity3d \
	-compute_wz \
	$common_args
