#!/usr/bin/env bash
# Get the initial conditions from a previous run.
# Requirements:
#  * `petibm-utilities`
#    (https://github.com/mesnardo/petibm-utilities; branch `petibm-0.2`).
# CLI: ./get-initial-conditions.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

IN_DIR="../2k35-meshA/0100000"
OUT_DIR="0100000.org"
mkdir -p $OUT_DIR
petibm-convert3d -name ux -source $IN_DIR/ux.h5 -destination $OUT_DIR/ux.dat \
	-nx 1070 -ny 1072 -nz 40 -periodic_z true -hdf52binary true
petibm-convert3d -name uy -source $IN_DIR/uy.h5 -destination $OUT_DIR/uy.dat \
	-nx 1071 -ny 1071 -nz 40 -periodic_z true -hdf52binary true
petibm-convert3d -name uz -source $IN_DIR/uz.h5 -destination $OUT_DIR/uz.dat \
	-nx 1071 -ny 1072 -nz 40 -periodic_z true -hdf52binary true
petibm-convert3d -name Hx -source $IN_DIR/Hx.h5 -destination $OUT_DIR/Hx.dat \
	-nx 1070 -ny 1072 -nz 40 -periodic_z true -hdf52binary true
petibm-convert3d -name Hy -source $IN_DIR/Hy.h5 -destination $OUT_DIR/Hy.dat \
	-nx 1071 -ny 1071 -nz 40 -periodic_z true -hdf52binary true
petibm-convert3d -name Hz -source $IN_DIR/Hz.h5 -destination $OUT_DIR/Hz.dat \
	-nx 1071 -ny 1072 -nz 40 -periodic_z true -hdf52binary true
petibm-convert3d -name phi -source $IN_DIR/phi.h5 -destination $OUT_DIR/phi.dat \
	-nx 1071 -ny 1072 -nz 40 -periodic_z true -hdf52binary true
