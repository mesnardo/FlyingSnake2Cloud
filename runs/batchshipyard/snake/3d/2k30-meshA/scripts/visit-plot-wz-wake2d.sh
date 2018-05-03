#!/usr/bin/env bash
# Plots a slice (at mid-spanwise) of the contours
# of the z-component of the vorticity field.
# CLI: ./visit-plot-wz-wake2d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

HOST="localhost"
DATA_DIR="$HOST:$SIMU_DIR"
OUT_DIR="$SIMU_DIR/figures"

visit -cli -nowin -s $ROOT_DIR/scripts/visit-plot-wz-wake2d.py \
	--wz-xdmf-path "$DATA_DIR/postprocessing/vorticity/wz.xmf" \
	--body-obj-path "$DATA_DIR/postprocessing/snake.obj" \
	--out-dir $OUT_DIR \
	--out-prefix "wz_wake2d_2k30_meshA_"
