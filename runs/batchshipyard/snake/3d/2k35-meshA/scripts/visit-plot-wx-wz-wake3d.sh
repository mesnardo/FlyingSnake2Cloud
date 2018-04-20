#!/usr/bin/env bash
# Plots the contours of the x- and z-components of the vorticity field.
# CLI: ./visit-plot-wx-wz-wake3d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

SCRIPT_PATH="$ROOT_DIR/scripts/plot-wx-wz-wake3d-visit.py"
HOST="theo.seas.gwu.edu"
DATA_DIR="$SIMU_DIR/postprocessing/vorticity"
OUT_DIR="$DATA_DIR/figures"

visit -cli -s $SCRIPT_PATH \
	--directory $HOST:$DATA_DIR \
	--out $OUT_DIR \
	--out-prefix "wx_wz_wake3d_2k35_meshA_"
