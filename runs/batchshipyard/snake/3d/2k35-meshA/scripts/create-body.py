"""
Generates the boundary points of a 3D cylinder with a flying-snake
cross-section at angle-of-attack 35 degrees.

We read the coordinates from the file `snakeAoA35.txt`, which contains the 2D
coordinates used by Anush with cuIBM.

The cylinder is extruded in the spanwise direction over a distance of 3.2c,
where c is the chord-length of the cross-section, which is 1.0 here.

We choose a spacing of 0.008c in the x-y plane and a spacing of 0.08c in the
spanwise direction.

We save the boundary coordinates into the file `flyingSnake3dAoA35.body`.
"""

import pathlib
from snake.geometry import Geometry2d


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent

filepath = root_dir / 'snakeAoA35.txt'
section = Geometry2d(file_path=filepath)
section.discretization(ds=0.008)
cylinder = section.extrusion(limits=(0.0, 3.2), ds=0.08)
filepath = root_dir / 'flyingSnake3dAoA35.body'
cylinder.write(file_path=filepath)
