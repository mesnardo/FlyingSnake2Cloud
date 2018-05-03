#!/usr/bin/env bash
# Creates XMF files for the x- and z- components of the 3D vorticity field.
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
--start 102400 --end 198400 --step 3200 \
--dt 0.0005
"

# Create XMF file for the x-component of the vorticity field.
echo "Creating XMF file for wx ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/wx.h5 \
	--grid-size 1279 999 79 \
	--variables wx \
	--output $OUT_DIR/wx.xmf \
	$common_args
# Create XMF file for the z-component of the vorticity field.
echo "Creating XMF file for wz ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/wz.h5 \
	--grid-size 1278 999 80 \
	--variables wz \
	--output $OUT_DIR/wz.xmf \
	$common_args
