"""
Write into .curve file a 2D slice of the boundary coordinates.
"""

import pathlib
import numpy


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent
out_dir = root_dir / 'postprocessing'

# Read 3D boundary points from file.
filepath = root_dir / 'flyingSnake3dAoA30.body'
with open(filepath, 'r') as infile:
  x, y, z = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True, skiprows=1)
# Keep a 2D slice of the cylinder.
nz = numpy.unique(z).size
nxy = x.size // nz
x, y = x[:nxy], y[:nxy]
# Write 2D boundary points into file.
filepath = out_dir / 'flyingSnake2dAoA30.curve'
filepath.parent.mkdir(parents=True, exist_ok=True)
with open(filepath, 'wb') as outfile:
  numpy.savetxt(outfile, numpy.c_[x, y])
