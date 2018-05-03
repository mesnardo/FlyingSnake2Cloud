#!/usr/bin/env bash
# Plots the contours of the x- and z-components of the vorticity field.
# CLI: ./visit-plot-wx-wz-crop-wake3d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

HOST="localhost"
DATA_DIR="$HOST:$SIMU_DIR"
OUT_DIR="$SIMU_DIR/figures"

visit -cli -nowin -s $ROOT_DIR/scripts/visit-plot-wx-wz-wake3d.py \
	--wx-xdmf-path "$DATA_DIR/postprocessing/vorticity-crop/wx.xmf" \
	--wz-xdmf-path "$DATA_DIR/postprocessing/vorticity-crop/wz.xmf" \
	--body-p3d-path "$DATA_DIR/postprocessing/snake.p3d" \
	--out-dir $OUT_DIR \
	--view-name "crop" \
	--out-prefix "wx_wz_crop_wake3d_2k35_meshBr2_"
