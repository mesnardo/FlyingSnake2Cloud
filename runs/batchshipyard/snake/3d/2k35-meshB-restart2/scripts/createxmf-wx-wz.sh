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
	--grid-size 1704 1705 79 \
	--data-dir $SIMU_DIR/postprocessing \
	--variables wx \
	--start 252800 --end 281600 --step 3200 \
	--dt 0.0005 \
	--output $SIMU_DIR/postprocessing/wx.xmf

# Create XMF file for the z-component of the vorticity field.
snake-createxmf \
	--grid-path $SIMU_DIR/postprocessing/grids/wz.h5 \
	--grid-size 1703 1705 80 \
	--data-dir $SIMU_DIR/postprocessing \
	--variables wz \
	--start 252800 --end 281600 --step 3200 \
	--dt 0.0005 \
	--output $SIMU_DIR/postprocessing/wz.xmf
