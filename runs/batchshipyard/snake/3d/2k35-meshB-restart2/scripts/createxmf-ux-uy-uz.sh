#!/usr/bin/env bash
# Create XMF files for the components of the 3D velocity field.
# CLI: ./createxmf-ux-uy-uz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)

AZURE_SNAKE="$SCRIPT_DIR/../../../../../.."
AZURE_SNAKE=$( cd $AZURE_SNAKE ; pwd -P )
export PATH="$AZURE_SNAKE/bin":$PATH

# Create XMF file for the x-component of the velocity field.
snake-createxmf \
	--grid-path $SIMU_DIR/grids/staggered-x.h5 \
	--grid-size 1703 1706 80 \
	--data-dir $SIMU_DIR/postprocessing \
	--variables ux \
	--start 252800 --end 281600 --step 3200 \
	--dt 0.0005 \
	--output $SIMU_DIR/postprocessing/ux.xmf

# Create XMF file for the y-component of the velocity field.
snake-createxmf \
	--grid-path $SIMU_DIR/grids/staggered-y.h5 \
	--grid-size 1704 1705 80 \
	--data-dir $SIMU_DIR/postprocessing \
	--variables uy \
	--start 252800 --end 281600 --step 3200 \
	--dt 0.0005 \
	--output $SIMU_DIR/postprocessing/uy.xmf

# Create XMF file for the z-component of the velocity field.
snake-createxmf \
	--grid-path $SIMU_DIR/grids/staggered-z.h5 \
	--grid-size 1704 1706 80 \
	--data-dir $SIMU_DIR/postprocessing \
	--variables uz \
	--start 252800 --end 281600 --step 3200 \
	--dt 0.0005 \
	--output $SIMU_DIR/postprocessing/uz.xmf
