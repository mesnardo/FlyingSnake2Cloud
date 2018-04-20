#!/usr/bin/env bash
# Gets the initial conditions by interpolating the final
# solution obtained on the coarser grid.
# The solution is also converted from PETSc binray format to HDF5.
# CLI: ./get-initial-conditions.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Set the directory that contains the data.
DATA_DIR="$ROOT_DIR/2k35-meshA/0100000"
GRID_DIR="$ROOT_DIR/2k35-meshA/grids"
# Set the output directory.
OUT_DIR="$SIMU_DIR/0100000-org"
OUT_GRID_DIR="$SIMU_DIR/grids"

# Set the common command-line arguments.
common_args="
-gridA_x_start -15.0 -gridA_x_end 15.0 \
-gridA_y_start -15.0 -gridA_y_end 15.0 \
-gridA_z_start 0.0 -gridA_z_end 3.2 \
-fieldA_periodic_z \
-gridB_x_start -15.0 -gridB_x_end 15.0 \
-gridB_y_start -15.0 -gridB_y_end 15.0 \
-gridB_z_start 0.0 -gridB_z_end 3.2
-fieldB_periodic_z
"

np=4

echo "Interpolating phi ..."
mpiexec -np $np petibm-interpolate \
	-gridA_path $GRID_DIR/cell-centered.h5 \
	-gridA_nx 1071 -gridA_ny 1072 -gridA_nz 40 \
	-fieldA_name phi \
	-fieldA_path $DATA_DIR/phi.h5 \
	-fieldA_bc_value 0.0 \
	-gridB_path $OUT_GRID_DIR/cell-centered.h5 \
	-gridB_nx 1704 -gridB_ny 1706 -gridB_nz 80 \
	-fieldB_name phi \
	-fieldB_path $OUT_DIR/phi.h5 \
	-fieldB_bc_value 0.0 \
	$common_args
echo "Converting phi ..."
mpiexec -np $np petibm-convert \
	-name phi \
	-source $OUT_DIR/phi.h5 -destination $OUT_DIR/phi.dat \
	-nx 1704 -ny 1706 -nz 80 -periodic_z -hdf52binary

echo "Interpolating ux ..."
mpiexec -np $np petibm-interpolate \
	-gridA_path $GRID_DIR/staggered-x.h5 \
	-gridA_nx 1070 -gridA_ny 1072 -gridA_nz 40 \
	-fieldA_name ux \
	-fieldA_path $DATA_DIR/ux.h5 \
	-fieldA_bc_value 1.0 \
	-gridB_path $OUT_GRID_DIR/staggered-x.h5 \
	-gridB_nx 1703 -gridB_ny 1706 -gridB_nz 80 \
	-fieldB_name ux \
	-fieldB_path $OUT_DIR/ux.h5 \
	-fieldB_bc_value 1.0 \
	$common_args
echo "Converting ux ..."
mpiexec -np $np petibm-convert \
	-name ux \
	-source $OUT_DIR/ux.h5 -destination $OUT_DIR/ux.dat \
	-nx 1703 -ny 1706 -nz 80 -periodic_z -hdf52binary

echo "Interpolating uy ..."
mpiexec -np $np petibm-interpolate \
	-gridA_path $GRID_DIR/staggered-y.h5 \
	-gridA_nx 1071 -gridA_ny 1071 -gridA_nz 40 \
	-fieldA_name uy \
	-fieldA_path $DATA_DIR/uy.h5 \
	-fieldA_bc_value 0.0 \
	-gridB_path $OUT_GRID_DIR/staggered-y.h5 \
	-gridB_nx 1704 -gridB_ny 1705 -gridB_nz 80 \
	-fieldB_name uy \
	-fieldB_path $OUT_DIR/uy.h5 \
	-fieldB_bc_value 0.0 \
	$common_args
echo "Converting uy ..."
mpiexec -np $np petibm-convert \
	-name uy \
	-source $OUT_DIR/uy.h5 -destination $OUT_DIR/uy.dat \
	-nx 1704 -ny 1705 -nz 80 -periodic_z -hdf52binary

echo "Interpolating uz ..."
mpiexec -np $np petibm-interpolate \
	-gridA_path $GRID_DIR/staggered-z.h5 \
	-gridA_nx 1071 -gridA_ny 1072 -gridA_nz 40 \
	-fieldA_name uz \
	-fieldA_path $DATA_DIR/uz.h5 \
	-fieldA_bc_value 0.0 \
	-gridB_path $OUT_GRID_DIR/staggered-z.h5 \
	-gridB_nx 1704 -gridB_ny 1706 -gridB_nz 80 \
	-fieldB_name uz \
	-fieldB_path $OUT_DIR/uz.h5 \
	-fieldB_bc_value 0.0 \
	$common_args
echo "Converting uz ..."
mpiexec -np $np petibm-convert \
	-name uz \
	-source $OUT_DIR/uz.h5 -destination $OUT_DIR/uz.dat \
	-nx 1704 -ny 1706 -nz 80 -periodic_z -hdf52binary

echo "Interpolating Hx ..."
mpiexec -np $np petibm-interpolate \
	-gridA_path $GRID_DIR/staggered-x.h5 \
	-gridA_nx 1070 -gridA_ny 1072 -gridA_nz 40 \
	-fieldA_name Hx \
	-fieldA_path $DATA_DIR/Hx.h5 \
	-fieldA_bc_value 0.0 \
	-gridB_path $OUT_GRID_DIR/staggered-x.h5 \
	-gridB_nx 1703 -gridB_ny 1706 -gridB_nz 80 \
	-fieldB_name Hx \
	-fieldB_path $OUT_DIR/Hx.h5 \
	-fieldB_bc_value 0.0 \
	$common_args
echo "Converting Hx ..."
mpiexec -np $np petibm-convert \
	-name Hx \
	-source $OUT_DIR/Hx.h5 -destination $OUT_DIR/Hx.dat \
	-nx 1703 -ny 1706 -nz 80 -periodic_z -hdf52binary

echo "Interpolating Hy ..."
mpiexec -np $np petibm-interpolate \
	-gridA_path $GRID_DIR/staggered-y.h5 \
	-gridA_nx 1071 -gridA_ny 1071 -gridA_nz 40 \
	-fieldA_name Hy \
	-fieldA_path $DATA_DIR/Hy.h5 \
	-fieldA_bc_value 0.0 \
	-gridB_path $OUT_GRID_DIR/staggered-y.h5 \
	-gridB_nx 1704 -gridB_ny 1705 -gridB_nz 80 \
	-fieldB_name Hy \
	-fieldB_path $OUT_DIR/Hy.h5 \
	-fieldB_bc_value 0.0 \
	$common_args
echo "Converting Hy ..."
mpiexec -np $np petibm-convert \
	-name Hy \
	-source $OUT_DIR/Hy.h5 -destination $OUT_DIR/Hy.dat \
	-nx 1704 -ny 1705 -nz 80 -periodic_z -hdf52binary

echo "Interpolating Hz ..."
mpiexec -np $np petibm-interpolate \
	-gridA_path $GRID_DIR/staggered-z.h5 \
	-gridA_nx 1071 -gridA_ny 1072 -gridA_nz 40 \
	-fieldA_name Hz \
	-fieldA_path $DATA_DIR/Hz.h5 \
	-fieldA_bc_value 0.0 \
	-gridB_path $OUT_GRID_DIR/staggered-z.h5 \
	-gridB_nx 1704 -gridB_ny 1706 -gridB_nz 80 \
	-fieldB_name Hz \
	-fieldB_path $OUT_DIR/Hz.h5 \
	-fieldB_bc_value 0.0 \
	$common_args
echo "Converting Hz ..."
mpiexec -np $np petibm-convert \
	-name Hz \
	-source $OUT_DIR/Hz.h5 -destination $OUT_DIR/Hz.dat \
	-nx 1704 -ny 1706 -nz 80 -periodic_z -hdf52binary
