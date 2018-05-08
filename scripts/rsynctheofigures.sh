#!/usr/bin/env bash
# FlyingSnake2Cloud: Rsync `figures` folders from Theo to local.

script_dir="$( cd "$(dirname "$0")" ; pwd -P )"
src_dir="theo:/tank/mesnardo/git/mesnardo/FlyingSnake2Cloud"
declare -a folders=(
"runs/batchshipyard/snake/3d/figures"
"runs/batchshipyard/snake/3d/1k35-meshA/figures"
"runs/batchshipyard/snake/3d/2k30-meshA/figures"
"runs/batchshipyard/snake/3d/2k35-meshA/figures"
"runs/batchshipyard/snake/3d/2k35-meshB/figures"
"runs/batchshipyard/snake/3d/2k35-meshB-restart1/figures"
"runs/batchshipyard/snake/3d/2k35-meshB-restart2/figures"
)
tmp_file="dirs.txt"
for folder in "${folders[@]}"; do
	echo $folder >> $tmp_file
done
dest_dir="$script_dir/figures-theo"
mkdir -p $dest_dir
rsync -arv -e ssh --files-from=$tmp_file $src_dir $dest_dir
rm -f $tmp_file
exit 0
