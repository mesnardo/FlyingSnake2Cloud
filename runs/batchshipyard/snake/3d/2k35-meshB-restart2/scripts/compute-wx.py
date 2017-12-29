"""
Computes the x-component of the 3D vorticity field at saved time steps.

Uses the mpiexec utility.
Requires the installation of `petibm-utilities`
(code available at https://github.com/mesnardo/petibm-utilities).
"""

import os
import subprocess
import argparse


parser_formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser_description = 'Compute the x-component of the vorticity field.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--np', '-np', dest='np',
                    type=int,
                    default=1,
                    help='Number of processes to run.')
args = parser.parse_args()

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.sep.join(script_dir.split(os.sep)[:-1])
out_dir = os.path.join(data_dir, 'postprocessing')
if not os.path.isdir(out_dir):
  os.makedirs(out_dir)

nx, ny, nz = 1704, 1706, 80
nstart, nend, nstep = 249600, 281600, 3200
args2 = ('-directory {} -output_directory {} '
         '-nstart {} -nend {} -nstep {} -nx {} -ny {} -nz {} '
         '-periodic_z true -compute_wx true -log_view -options_left'
         .format(data_dir, out_dir, nstart, nend, nstep, nx, ny, nz))
subprocess.call('mpiexec -np {} petibm-vorticity3d {}'.format(args.np, args2),
                shell=True)
