"""
Create the 3D snake geometry by extruding the section in the spanwise direction
and save the geometry into file in OBJ format.
"""

import os
import pathlib
import numpy

from snake.openfoam import OBJFile


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent
out_dir = root_dir / 'postprocessing'

# Read the 2D geometry from file.
filepath = root_dir / 'snakeAoA30.txt'
with open(filepath, 'r') as infile:
  x, y = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)
# Save the 2D geometry into file using PetIBM format.
filepath = root_dir / 'snakeAoA30_tmp.txt'
with open(filepath, 'w') as outfile:
  outfile.write('{}\n'.format(x.size))
with open(filepath, 'ab') as outfile:
  numpy.savetxt(outfile, numpy.c_[x, y], delimiter='\t')
# Create and write the 3D OBJ snake geometry.
body = OBJFile.Body2d(filepath,
                      name='snake',
                      extrusion_limits=[0.0, 3.2])
out_dir.mkdir(parents=False, exist_ok=True)
body.write(save_directory=str(out_dir))
# Remove temporary file.
os.remove(filepath)
