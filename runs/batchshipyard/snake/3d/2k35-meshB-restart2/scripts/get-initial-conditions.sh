#!/usr/bin/env bash
# Gets the initial conditions by copying the numerical solution
# obtained from the previous run at time step 195200.
# CLI: ./get-initial-conditions.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Set the directory that contains the data.
DATA_DIR="$ROOT_DIR/2k35-meshB-restart1/0249600"
GRID_DIR="$ROOT_DIR/2k35-meshB-restart1/grids"
# Set the output directory.
OUT_DIR="$SIMU_DIR/0249600-org"
OUT_GRID_DIR="$SIMU_DIR/grids-org"

# Copy grids and numerical solution.
cp -r $GRID_DIR $OUT_GRID_DIR
cp -r $DATA_DIR $OUT_DIR
