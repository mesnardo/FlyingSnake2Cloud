#!/usr/bin/env bash
# Plots a slice (at mid-spanwise) of the contours
# of the z-component of the vorticity field.
# CLI: ./visit-plot-wz-wake2d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

HOST="theo.seas.gwu.edu"
DATA_DIR="$HOST:/tank/mesnardo/git/mesnardo/FlyingSnake2Cloud/runs/batchshipyard/snake/3d/2k35-meshB-restart1"
OUT_DIR="figures"

visit -cli -s $ROOT_DIR/scripts/visit-plot-wz-wake2d.py \
	--wz-xdmf-path "$DATA_DIR/postprocessing/vorticity/wz.xmf" \
	--body-obj-path "$DATA_DIR/postprocessing/snake.obj" \
	--out-dir $OUT_DIR \
	--out-prefix "wz_wake2d_2k35_meshBr1_"
