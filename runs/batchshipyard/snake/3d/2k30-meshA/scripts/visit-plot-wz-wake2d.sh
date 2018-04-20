#!/usr/bin/env bash
# Plots a slice (at mid-spanwise) of the contours
# of the z-component of the vorticity field.
# CLI: ./visit-plot-wz-wake2d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

SCRIPT_PATH="$ROOT_DIR/scripts/plot-wz-wake2d-visit.py"
HOST="theo.seas.gwu.edu"
DATA_DIR="$SIMU_DIR/postprocessing/vorticity"
OUT_DIR="$DATA_DIR/figures"

visit -cli -s $SCRIPT_PATH \
	--directory $HOST:$DATA_DIR \
	--out $OUT_DIR \
	--out-prefix "wz_wake2d_2k30_meshA_"
