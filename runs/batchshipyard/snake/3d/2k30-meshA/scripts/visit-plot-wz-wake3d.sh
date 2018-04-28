#!/usr/bin/env bash
# Plots the contours of the z-component of the vorticity field.
# CLI: ./visit-plot-wz-wake3d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

HOST="theo.seas.gwu.edu"
DATA_DIR="$HOST:/tank/mesnardo/git/mesnardo/FlyingSnake2Cloud/runs/batchshipyard/snake/3d/2k30-meshA"
OUT_DIR="figures"

visit -cli -s $ROOT_DIR/scripts/visit-plot-wz-wake3d.py \
	--wz-xdmf-path "$DATA_DIR/postprocessing/vorticity/wz.xmf" \
	--body-obj-path "$DATA_DIR/postprocessing/snake.obj" \
	--out-dir $OUT_DIR \
	--out-prefix "wz_wake3d_2k30_meshA_"
