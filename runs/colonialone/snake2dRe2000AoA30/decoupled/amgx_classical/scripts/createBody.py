"""
Write the snake cross-section into file compatible with PetIBM.
"""

import os
import numpy


if not os.environ.get('AZ_SNAKE'):
  raise KeyError('Environment variable AZ_SNAKE is not set')

filepath = os.path.join(os.environ['AZ_SNAKE'], 'resources', 'geometries',
                        'snakeAoA30.txt')
with open(filepath, 'r') as infile:
  x, y = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)

N = x.size
filepath = os.path.join(os.getcwd(), 'snakeAoA30.body')
with open(filepath, 'wb') as outfile:
  numpy.savetxt(outfile, numpy.c_[x, y], fmt='%0.6f',
                header=str(N), comments='')
