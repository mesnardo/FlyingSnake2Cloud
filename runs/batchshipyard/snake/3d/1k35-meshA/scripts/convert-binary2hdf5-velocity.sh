#!/usr/bin/env bash
# Converts the velocity field from PETSc binary format to HDF5.
# CLI: ./convert-binary2hdf5-velocity.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Set the directory that contains the data.
DATA_DIR=$SIMU_DIR
# Set the output directory.
OUT_DIR="$SIMU_DIR/postprocessing/convert"

np=4

for ((i=100000; i<=200000; i+=2000)); do
	FOLDER=$(printf "%07.0f" $i)
	echo "[time-step $i] Converting ux ..."
	mpiexec -np $np petibm-convert \
		-name ux \
		-source $DATA_DIR/$FOLDER/ux.dat -destination $OUT_DIR/$FOLDER/ux.h5 \
		-nx 1070 -ny 1072 -nz 40 -periodic_z
	echo "[time-step $i] Converting uy ..."
	mpiexec -np $np petibm-convert \
		-name uy \
		-source $DATA_DIR/$FOLDER/uy.dat -destination $OUT_DIR/$FOLDER/uy.h5 \
		-nx 1071 -ny 1071 -nz 40 -periodic_z
	echo "[time-step $i] Converting uz ..."
	mpiexec -np $np petibm-convert \
		-name uz \
		-source $DATA_DIR/$FOLDER/uz.dat -destination $OUT_DIR/$FOLDER/uz.h5 \
		-nx 1071 -ny 1072 -nz 40 -periodic_z
done
