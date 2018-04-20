#!/usr/bin/env bash
# Crops the pressure field and the velocity components.
# ./crop-phi-ux-uy-uz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)

source $(dirname $SIMU_DIR)/bashrc

# Set the directory that contains the data.
DATA_DIR=$SIMU_DIR
# Set the output directory.
OUT_DIR="$SIMU_DIR/postprocessing/crop"

# Set the common command-line arguments.
common_args="
-data_directory $DATA_DIR \
-output_directory $OUT_DIR \
-nstart 5000 -nend 100000 -nstep 5000 \
-x_start -1.0 -x_end 5.0 \
-y_start -2.0 -y_end 2.0 \
-z_start 0.0 -z_end 3.2
"
np=2

echo "Cropping phi ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1071 -gridA_ny 1072 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/cell-centered.h5 \
	-gridA_name phi -fieldA_name phi \
	$common_args
echo "Cropping ux ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1070 -gridA_ny 1072 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/staggered-x.h5 \
	-gridA_name ux -fieldA_name ux \
	$common_args
echo "Cropping uy ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1071 -gridA_ny 1071 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/staggered-y.h5 \
	-gridA_name uy -fieldA_name uy \
	$common_args
echo "Cropping uz ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1071 -gridA_ny 1072 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/staggered-z.h5 \
	-gridA_name uz -fieldA_name uz \
	$common_args
