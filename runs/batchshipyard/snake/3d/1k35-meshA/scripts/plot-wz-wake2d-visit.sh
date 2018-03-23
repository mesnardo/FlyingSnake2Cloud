#!/usr/bin/env bash
# Plot a slice (at mid-spanwise) of contour
# of the z-component of the vorticity field.
# CLI: ./plot-wz-wake2d-visit.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

SCRIPT_PATH="$ROOT_DIR/scripts/plot-wz-wake2d-visit.py"
HOST="theo.seas.gwu.edu"
DATA_DIR="$SIMU_DIR/postprocessing"
OUT_DIR="$SIMU_DIR/figures"

visit -cli -s $SCRIPT_PATH \
	--directory $HOST:$DATA_DIR \
	--out $OUT_DIR \
	--out-prefix "wz_wake2d_1k35_meshA_"
