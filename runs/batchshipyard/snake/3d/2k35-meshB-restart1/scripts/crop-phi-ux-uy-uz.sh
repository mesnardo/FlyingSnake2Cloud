#!/usr/bin/env bash
# Crops the pressure field and the velocity components.
# ./crop-phi-ux-uy-uz.sh

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
-input_binary \
-output_directory $OUT_DIR \
-nstart 195200 -nend 249600 -nstep 3200 \
-x_start -0.99568 -x_end 5.99569 \
-y_start -1.99801 -y_end 1.998 \
-z_start 0.02 -z_end 3.20001
"
np=4

echo "Cropping phi ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1704 -gridA_ny 1706 -gridA_nz 80 \
	-gridA_path $DATA_DIR/grids/cell-centered.h5 \
	-gridA_name phi -fieldA_name phi \
	$common_args
mv $OUT_DIR/grids/phi.h5 $OUT_DIR/grids/cell-centered.h5
echo "Cropping ux ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1703 -gridA_ny 1706 -gridA_nz 80 \
	-gridA_path $DATA_DIR/grids/staggered-x.h5 \
	-gridA_name ux -fieldA_name ux \
	$common_args
mv $OUT_DIR/grids/ux.h5 $OUT_DIR/grids/staggered-x.h5
echo "Cropping uy ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1704 -gridA_ny 1705 -gridA_nz 80 \
	-gridA_path $DATA_DIR/grids/staggered-y.h5 \
	-gridA_name uy -fieldA_name uy \
	$common_args
mv $OUT_DIR/grids/uy.h5 $OUT_DIR/grids/staggered-y.h5
echo "Cropping uz ..."
mpiexec -np $np petibm-crop \
	-gridA_nx 1704 -gridA_ny 1706 -gridA_nz 80 \
	-gridA_path $DATA_DIR/grids/staggered-z.h5 \
	-gridA_name uz -fieldA_name uz \
	$common_args
mv $OUT_DIR/grids/uz.h5 $OUT_DIR/grids/staggered-z.h5
