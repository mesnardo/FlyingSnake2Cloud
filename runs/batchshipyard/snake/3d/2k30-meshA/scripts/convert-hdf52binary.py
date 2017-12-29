"""
Convert HDF5 files to binary files.
"""

import os
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.sep.join(script_dir.split(os.sep)[:-2])
simu_dir = os.sep.join(script_dir.split(os.sep)[:-1])

petsc_dir = os.path.join(os.environ['HOME'], 'src', 'petsc', '3.7.4')
petsc_arch = 'linux-gnu-opt'
os.environ['PATH'] = (os.path.join(petsc_dir, petsc_arch, 'bin') +
                      os.pathsep +
                      os.environ['PATH'])
utilities_dir = os.path.join(os.environ['HOME'], 'build', 'petibm-utilities',
                             'master', 'install')
os.environ['PATH'] = (os.path.join(utilities_dir, 'bin') +
                      os.pathsep +
                      os.environ['PATH'])

variables = {'ux': (1070, 1072, 40),
             'uy': (1071, 1071, 40),
			 'uz': (1071, 1072, 40),
			 'Hx': (1070, 1072, 40),
			 'Hy': (1071, 1071, 40),
			 'Hz': (1071, 1072, 40),
			 'phi': (1071, 1072, 40)}
np = 1
time_steps = [100000]
for i in time_steps:
  folder = '{:0>7}'.format(i)
  source_dir = os.path.join(simu_dir, folder)
  dest_dir = os.path.join(simu_dir, folder)
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)
  for key in variables.keys():
    print('[time step {}] Converting {} ...'.format(i, key))
    source_path = os.path.join(source_dir, key + '.h5')
    dest_path = os.path.join(dest_dir, key + '.dat')
    args = ('-name {} -source {} -destination {} -nx {} -ny {} -nz {} '
            '-periodic_z true -hdf52binary true'
            .format(key, source_path, dest_path, *variables[key]))
    subprocess.call('mpiexec -np {} petibm-convert3d {}'.format(np, args),
                    shell=True)
