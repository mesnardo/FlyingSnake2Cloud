#!/usr/bin/env bash
# Computes the x- and z- components of the 3D vorticity field.
# Requirements:
#  * mpiexec.
#	 * `petibm-utilities`
#    (https://github.com/mesnardo/petibm-utilities; branch `petibm-0.2`).
# CLI: ./compute-wx-wz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Compute the x-component of the vorticity field.
mpiexec -np 12 petibm-vorticity3d \
	-directory $SIMU_DIR/postprocessing \
	-output_directory $SIMU_DIR/postprocessing \
	-grid_directory $SIMU_DIR/grids \
	-nstart 252800 -nend 281600 -nstep 3200 \
	-nx 1704 -ny 1706 -nz 80 \
	-periodic_z true \
	-compute_wx true -compute_wz false \
	-options_left
# Compute the z-component of the vorticity field.
mpiexec -np 12 petibm-vorticity3d \
	-directory $SIMU_DIR/postprocessing \
	-output_directory $SIMU_DIR/postprocessing \
	-grid_directory $SIMU_DIR/grids \
	-nstart 252800 -nend 281600 -nstep 3200 \
	-nx 1704 -ny 1706 -nz 80 \
	-periodic_z true \
	-compute_wx false -compute_wz true \
	-options_left
