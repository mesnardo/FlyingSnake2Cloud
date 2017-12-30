#!/bin/sh

SCRIPT_PATH="plot-wz-wx-visit.py"
HOSTNAME="theo.seas.gwu.edu"
DATA_DIR="/tank/mesnardo/git/mesnardo/FlyingSnake2Cloud/runs/batchshipyard/snake/3d/2k35-meshA/postprocessing"
OUT_DIR=$PWD
visit -cli -s $SCRIPT_PATH \
	--host $HOSTNAME \
	--directory $DATA_DIR \
	--out $OUT_DIR
