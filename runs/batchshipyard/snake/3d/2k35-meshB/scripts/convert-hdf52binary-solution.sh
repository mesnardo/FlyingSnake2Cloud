#!/usr/bin/env bash
# Converts the initial solution from HDF5 to PETSc binary format.
# CLI: ./convert-hdf52binary-solution.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Set the directory that contains the data.
DATA_DIR="$ROOT_DIR/2k35-meshA/postprocessing/interpolate/0100000"
# Set the output directory.
OUT_DIR="$SIMU_DIR/0100000-org"

np=4

echo "Converting phi ..."
mpiexec -np $np petibm-convert \
	-name phi \
	-source $DATA_DIR/phi.h5 \
	-destination $OUT_DIR/phi.dat \
	-nx 1704 -ny 1706 -nz 80 -periodic_z \
	-hdf52binary
echo "Converting ux ..."
mpiexec -np $np petibm-convert \
	-name ux \
	-source $DATA_DIR/ux.h5 \
	-destination $OUT_DIR/ux.dat \
	-nx 1703 -ny 1706 -nz 80 -periodic_z \
	-hdf52binary
echo "Converting uy ..."
mpiexec -np $np petibm-convert \
	-name uy \
	-source $DATA_DIR/uy.h5 \
	-destination $OUT_DIR/uy.dat \
	-nx 1704 -ny 1705 -nz 80 -periodic_z \
	-hdf52binary
echo "Converting uz ..."
mpiexec -np $np petibm-convert \
	-name uz \
	-source $DATA_DIR/uz.h5 \
	-destination $OUT_DIR/uz.dat \
	-nx 1704 -ny 1706 -nz 80 -periodic_z \
	-hdf52binary
echo "Converting Hx ..."
mpiexec -np $np petibm-convert \
	-name Hx \
	-source $DATA_DIR/Hx.h5 \
	-destination $OUT_DIR/Hx.dat \
	-nx 1703 -ny 1706 -nz 80 -periodic_z \
	-hdf52binary
echo "Converting Hy ..."
mpiexec -np $np petibm-convert \
	-name Hy \
	-source $DATA_DIR/Hy.h5 \
	-destination $OUT_DIR/Hy.dat \
	-nx 1704 -ny 1705 -nz 80 -periodic_z \
	-hdf52binary
echo "Converting Hz ..."
mpiexec -np $np petibm-convert \
	-name Hz \
	-source $DATA_DIR/Hz.h5 \
	-destination $OUT_DIR/Hz.dat \
	-nx 1704 -ny 1706 -nz 80 -periodic_z \
	-hdf52binary
