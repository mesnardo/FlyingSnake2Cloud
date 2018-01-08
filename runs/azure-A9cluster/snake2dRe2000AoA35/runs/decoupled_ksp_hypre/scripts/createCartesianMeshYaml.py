"""
Creates a YAML file with info about the structured Cartesian mesh that will be
parsed by PetIBM.

Creates a 2D structured Cartesian grid.
"""

import numpy
from matplotlib import pyplot
from snake.cartesianMesh import CartesianStructuredMesh


# info about the 2D structured Cartesian grid
width = 0.004  # minimum grid spacing in the x- and y- directions
info = [{'direction': 'x', 'start': -15.0,
         'subDomains': [{'end': -0.52,
                         'width': width,
                         'stretchRatio': 1.01,
                         'reverse': True,
                         'precision': 2},
                        {'end': 3.48,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': 1.01,
                         'precision': 2}]},
        {'direction': 'y', 'start': -15.0,
         'subDomains': [{'end': -2.0,
                         'width': width,
                         'stretchRatio': 1.01,
                         'reverse': True,
                         'precision': 2},
                        {'end': 2.0,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': 1.01,
                         'precision': 2}]}]

mesh = CartesianStructuredMesh()
mesh.create(info)
mesh.print_parameters()
mesh.write_yaml_file('cartesianMesh.yaml')

filepath = 'xgrid.dat'
mesh.write(filepath, direction='x')
with open(filepath, 'r') as infile:
  x = numpy.loadtxt(infile, dtype=numpy.float64)
filepath = 'ygrid.dat'
mesh.write(filepath, direction='y')
with open(filepath, 'r') as infile:
  y = numpy.loadtxt(infile, dtype=numpy.float64)

fig, ax = pyplot.subplots(figsize=(10.0, 10.0))
ax.grid()
for val in x:
  ax.axvline(val, ymin=y[0], ymax=y[-1])
for val in y:
  ax.axhline(val, xmin=x[0], xmax=x[-1])
ax.set_aspect('equal')
ax.set_xlim(x[0], x[-1])
ax.set_ylim(y[0], y[-1])
pyplot.show()
