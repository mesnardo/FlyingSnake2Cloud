"""
Computes the z-component of the 3D vorticity field at saved time steps.

Uses the mpiexec utility.
Requires the installation of `petibm-utilities`
(code available at https://github.com/mesnardo/petibm-utilities).
"""

import os
import subprocess
import argparse


parser_formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser_description = 'Compute the z-component of the vorticity field.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--np', '-np', dest='np',
                    type=int,
                    default=1,
                    help='Number of processes to run.')
args = parser.parse_args()

script_dir = os.path.dirname(os.path.realpath(__file__))
simu_dir = os.sep.join(script_dir.split(os.sep)[:-1])
data_dir = os.path.join(simu_dir, 'postprocessing')
grid_dir = os.path.join(simu_dir, 'grids')
out_dir = data_dir
if not os.path.isdir(out_dir):
  os.makedirs(out_dir)


nx, ny, nz = 1704, 1706, 80
nstart, nend, nstep = 100000, 100000, 3200
args2 = ('-directory {} -output_directory {} -grid_directory {} '
         '-nstart {} -nend {} -nstep {} -nx {} -ny {} -nz {} '
         '-periodic_z true -compute_wz true '
         '-log_view -options_left'
         .format(data_dir, out_dir, grid_dir, nstart, nend, nstep, nx, ny, nz))
subprocess.call('mpiexec -np {} petibm-vorticity3d {}'.format(args.np, args2),
                shell=True)
nstart, nend, nstep = 102400, 198400, 3200
args2 = ('-directory {} -output_directory {} -grid_directory {} '
         '-nstart {} -nend {} -nstep {} -nx {} -ny {} -nz {} '
         '-periodic_z true -compute_wz true '
         '-log_view -options_left'
         .format(data_dir, out_dir, grid_dir, nstart, nend, nstep, nx, ny, nz))
subprocess.call('mpiexec -np {} petibm-vorticity3d {}'.format(args.np, args2),
                shell=True)
