#!/usr/bin/env bash
# Creates XMF files for the pressure field and the velocity components.
# CLI: ./createxmf-phi-ux-uy-uz-crop.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)

source $(dirname $SIMU_DIR)/bashrc

# Set the directory that contains the data.
DATA_DIR="$SIMU_DIR/postprocessing/crop"
# Set the output directory.
OUT_DIR=$DATA_DIR
mkdir -p $OUT_DIR

# Set the common command-line arguments.
common_args="
--data-dir $DATA_DIR \
--start 5000 --end 100000 --step 5000 \
--dt 0.001
"

# Create XMF file for the pressure field.
echo "Creating XMF file for phi ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/phi.h5 \
	--grid-size 654 500 40 \
	--variables phi \
	--output $OUT_DIR/phi.xmf \
	$common_args

# Create XMF file for the x-component of the velocity field.
echo "Creating XMF file for ux ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/ux.h5 \
	--grid-size 655 500 40 \
	--variables ux \
	--output $OUT_DIR/ux.xmf \
	$common_args

# Create XMF file for the y-component of the velocity field.
echo "Creating XMF file for uy ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/uy.h5 \
	--grid-size 654 499 40 \
	--variables uy \
	--output $OUT_DIR/uy.xmf \
	$common_args

# Create XMF file for the z-component of the velocity field.
echo "Creating XMF file for uz ..."
snake-createxmf \
	--grid-path $DATA_DIR/grids/uz.h5 \
	--grid-size 654 500 39 \
	--variables uz \
	--output $OUT_DIR/uz.xmf \
	$common_args
