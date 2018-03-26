#!/usr/bin/env bash
# Create XMF files for the x- and z- components of the 3D vorticity field.
# CLI: ./createxmf-wx-wz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)

AZURE_SNAKE="$SCRIPT_DIR/../../../../../.."
AZURE_SNAKE=$( cd $AZURE_SNAKE ; pwd -P )
export PATH="$AZURE_SNAKE/bin":$PATH

# Create XMF file for the x-component of the vorticity field.
snake-createxmf \
	--grid-path $SIMU_DIR/postprocessing/grids/wx.h5 \
	--grid-size 1071 1071 39 \
	--data-dir $SIMU_DIR/postprocessing \
	--variables wx \
	--start 5000 --end 100000 --step 5000 \
	--dt 0.001 \
	--output $SIMU_DIR/postprocessing/wx.xmf

# Create XMF file for the z-component of the vorticity field.
snake-createxmf \
	--grid-path $SIMU_DIR/postprocessing/grids/wz.h5 \
	--grid-size 1070 1071 40 \
	--data-dir $SIMU_DIR/postprocessing \
	--variables wz \
	--start 5000 --end 100000 --step 5000 \
	--dt 0.001 \
	--output $SIMU_DIR/postprocessing/wz.xmf
