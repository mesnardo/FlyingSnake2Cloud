#!/usr/bin/env bash
# Crops the velocity components.
# ./crop-ux-uy-uz.sh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SIMU_DIR=$(dirname $SCRIPT_DIR)
ROOT_DIR=$(dirname $SIMU_DIR)

source $ROOT_DIR/bashrc

# Set the directory that contains the data.
DATA_DIR=$SIMU_DIR
# Set the output directory.
OUT_DIR="$SIMU_DIR/postprocessing/solution-crop"

# Set the common command-line arguments.
common_args="
-data_directory $DATA_DIR \
-output_directory $OUT_DIR \
-nstart 5000 -nend 100000 -nstep 5000 \
-x_start -0.99288 -x_end 5.9776 \
-y_start -1.99601 -y_end 1.99601 \
-z_start 0.04 -z_end 3.20001
"
np=1

echo "Cropping ux ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1070 -gridA_ny 1072 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/staggered-x.h5 \
	-gridA_name ux -fieldA_name ux \
	$common_args
mv $OUT_DIR/grids/ux.h5 $OUT_DIR/grids/staggered-x.h5
echo "Cropping uy ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1071 -gridA_ny 1071 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/staggered-y.h5 \
	-gridA_name uy -fieldA_name uy \
	$common_args
mv $OUT_DIR/grids/uy.h5 $OUT_DIR/grids/staggered-y.h5
echo "Cropping uz ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1071 -gridA_ny 1072 -gridA_nz 40 \
	-gridA_path $DATA_DIR/grids/staggered-z.h5 \
	-gridA_name uz -fieldA_name uz \
	$common_args
mv $OUT_DIR/grids/uz.h5 $OUT_DIR/grids/staggered-z.h5
