"""
Creates the time-step folders and add empty files for the numerical solution
to be written.
"""

import os
import numpy


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

nstart = 0
nt = 200000
nsave = 2500
nrestart = 20000

filenames = ['ux.h5', 'uy.h5', 'phi.h5', 'fTilde.h5']
extra_filenames = ['Hx.h5', 'Hy.h5']

steps = numpy.arange(nstart, nstart + nt + 1, nsave)
for step in steps[1:]:
  folder = os.path.join(root_dir, '{:0>7}'.format(step))
  os.makedirs(folder)
  for filename in filenames:
    os.system('touch {}'.format(os.path.join(folder, filename)))
  if step % nrestart == 0:
    for filename in extra_filenames:
      os.system('touch {}'.format(os.path.join(folder, filename)))
