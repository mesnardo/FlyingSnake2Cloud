#!/usr/bin/env bash
# Create XMF files for the x- and z-components of the 3D vorticity field.
# CLI: ./createxmf-wx-wz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Set the directory that contains the data.
DATA_DIR="$SIMU_DIR/postprocessing/vorticity-crop"
# Set the output directory.
OUT_DIR=$DATA_DIR

# Set the common command-line arguments.
common_args="
--data-dir $DATA_DIR \
--start 100000 --end 200000 --step 2000 \
--dt 0.001
"

# Create XMF file for the x-component of the vorticity field.
echo "Creating XMF file for wx ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/wx.h5 \
	--grid-size 690 499 39 \
	--variables wx \
	--output $OUT_DIR/wx.xmf \
	$common_args

# Create XMF file for the z-component of the vorticity field.
echo "Creating XMF file for wz ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/wz.h5 \
	--grid-size 689 499 40 \
	--variables wz \
	--output $OUT_DIR/wz.xmf \
	$common_args
