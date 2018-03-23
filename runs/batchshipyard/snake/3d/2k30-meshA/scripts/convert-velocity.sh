#!/usr/bin/env bash
# Convert the velocity field from PETSc format to HDF5.
# Requirements:
#  * `petibm-utilities`
#    (https://github.com/mesnardo/petibm-utilities; branch `petibm-0.2`).

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

IN_DIR=$SIMU_DIR
OUT_DIR="$SIMU_DIR/postprocessing"
for ((i=100000; i<=200000; i+=2000)); do
	FOLDER=$(printf "%07.0f" $i)
	mkdir -p $OUT_DIR/$FOLDER
	echo "[time-step $i] Converting ux ..."
	petibm-convert3d -name ux \
		-source $IN_DIR/$FOLDER/ux.dat -destination $OUT_DIR/$FOLDER/ux.h5 \
		-nx 1070 -ny 1072 -nz 40 -periodic_z true -hdf52binary false
	echo "[time-step $i] Converting uy ..."
	petibm-convert3d -name uy \
		-source $IN_DIR/$FOLDER/uy.dat -destination $OUT_DIR/$FOLDER/uy.h5 \
		-nx 1071 -ny 1071 -nz 40 -periodic_z true -hdf52binary false
	echo "[time-step $i] Converting uz ..."
	petibm-convert3d -name uz \
		-source $IN_DIR/$FOLDER/uz.dat -destination $OUT_DIR/$FOLDER/uz.h5 \
		-nx 1071 -ny 1072 -nz 40 -periodic_z true -hdf52binary false
done
