"""
Converts the 3D velocity field from PETSc binary to HDF5.
"""

import os
import subprocess
import argparse


script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.sep.join(script_dir.split(os.sep)[:-1])
out_dir = os.path.join(data_dir, 'postprocessing')

parser_formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser_description = 'Convert the velocity field from PETSc binary to HDF5.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--np', '-np', dest='np',
                    type=int,
                    default=1,
                    help='Number of processes to run.')
args = parser.parse_args()

variables = {'ux': (1070, 1072, 40),
             'uy': (1071, 1071, 40),
             'uz': (1071, 1072, 40)}

for i in range(100000, 200000 + 1, 2000):
  folder = '{:0>7}'.format(i)
  source_dir = os.path.join(data_dir, folder)
  dest_dir = os.path.join(out_dir, folder)
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)
  for key in variables.keys():
    print('[time step {}] Converting {} ...'.format(i, key))
    source_path = os.path.join(source_dir, key + '.dat')
    dest_path = os.path.join(dest_dir, key + '.h5')
    args2 = ('-name {} -source {} -destination {} -nx {} -ny {} -nz {} '
             '-periodic_z true -hdf52binary false'
             .format(key, source_path, dest_path, *variables[key]))
    subprocess.call('mpiexec -np {} petibm-convert3d {}'.format(args.np,
                                                                args2),
                    shell=True)
