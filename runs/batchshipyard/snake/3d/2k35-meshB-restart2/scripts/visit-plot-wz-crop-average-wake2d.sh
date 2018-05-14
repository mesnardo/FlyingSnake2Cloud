#!/usr/bin/env bash
# Plots a pseudocolor of the spanwise-averaged z-component
# of the vorticity field.
# CLI: ./visit-plot-wz-crop-average-wake2d.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

HOST="localhost"
DATA_DIR="$HOST:$SIMU_DIR"
OUT_DIR="$SIMU_DIR/figures"

visit -cli -nowin -s $ROOT_DIR/scripts/visit-plot-wz-crop-average-wake2d.py \
	--wz-xdmf-path "$DATA_DIR/postprocessing/vorticity-crop/spanwise-average/wz.xmf" \
	--body-curve-path "$DATA_DIR/postprocessing/flyingSnake2dAoA35.curve" \
	--out-dir $OUT_DIR \
	--out-prefix "wz_crop_average_wake2d_2k35_meshBr2_"

visit -cli -nowin -s $ROOT_DIR/scripts/visit-plot-wz-crop-average-wake2d.py \
	--wz-xdmf-path "$DATA_DIR/postprocessing/vorticity-crop/spanwise-average/wz.xmf" \
	--body-curve-path "$DATA_DIR/postprocessing/flyingSnake2dAoA35.curve" \
	--view -1.00 2.00 -1.50 1.50 \
	--out-dir $OUT_DIR \
	--out-prefix "wz_crop_average_wake2d_zoom_2k35_meshBr2_"
