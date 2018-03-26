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

mpiexec -np 4 petibm-vorticity3d \
	-directory $SIMU_DIR \
	-output_directory $SIMU_DIR/postprocessing \
	-grid_directory $SIMU_DIR/grids \
	-nstart 5000 -nend 100000 -nstep 5000 \
	-nx 1071 -ny 1072 -nz 40 \
	-periodic_z true \
	-compute_wx true -compute_wz true \
	-log_view ascii:stdout-compute-wx-wz.txt \
	-options_left
