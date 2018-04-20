#!/usr/bin/env bash
# Crops the x- and z-components of the voriticity field.
# CLI: ./crop-wx-wz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)

source $(dirname $SIMU_DIR)/bashrc

# Set the directory that contains the data.
DATA_DIR="$SIMU_DIR/postprocessing/vorticity"
# Set the output directory.
OUT_DIR="$SIMU_DIR/postprocessing/crop"

# Set common command-line arguments.
common_args="
-data_directory $DATA_DIR \
-output_directory $OUT_DIR \
-nstart 5000 -nend 100000 -nstep 5000 \
-x_start -1.0 -x_end 5.0 \
-y_start -2.0 -y_end 2.0 \
-z_start 0.0 -z_end 3.2
"
np=2

echo "Cropping wx ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1071 -gridA_ny 1071 -gridA_nz 39 \
	-gridA_path $DATA_DIR/grids/wx.h5 \
	-gridA_name wx -fieldA_name wx \
	$common_args

echo "Cropping wz ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1070 -gridA_ny 1071 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/wz.h5 \
	-gridA_name wz -fieldA_name wz \
	$common_args
