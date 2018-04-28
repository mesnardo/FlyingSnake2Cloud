#!/usr/bin/env bash
# Plots the contours of the x- and z-components of the vorticity field.
# CLI: ./visit-plot-wx-wz-wake3d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

HOST="theo.seas.gwu.edu"
DATA_DIR="$HOST:/tank/mesnardo/git/mesnardo/FlyingSnake2Cloud/runs/batchshipyard/snake/3d/2k35-meshB-restart2"
OUT_DIR="figures"

visit -cli -s $ROOT_DIR/scripts/visit-plot-wx-wz-wake3d.py \
	--wx-xdmf-path "$DATA_DIR/postprocessing/vorticity/wx.xmf" \
	--wz-xdmf-path "$DATA_DIR/postprocessing/vorticity/wz.xmf" \
	--body-p3d-path "$DATA_DIR/postprocessing/snake.p3d" \
	--out-dir $OUT_DIR \
	--out-prefix "wx_wz_wake3d_2k35_meshBr2_"
