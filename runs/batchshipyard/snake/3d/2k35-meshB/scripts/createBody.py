"""
Generates the boundary points of a 3D cylinder with a flying-snake
cross-section at angle-of-attack 35 degrees.

We read the coordinates from the file `snakeAoA35.txt`, which contains the 2D
coordinates used by Anush with cuIBM.

The cylinder is extruded in the spanwise direction over a distance of 3.2c,
where c is the chord-length of the cross-section, which is 1.0 here.

We choose a spacing of 0.004c in the x-y plane and a spacing of 0.04c in the
spanwise direction.

We save the boundary coordinates into the file `flyingSnake3dAoA35.body`.
"""

from snake.geometry import Geometry2d


section = Geometry2d(file_path='snakeAoA35.txt')
section.discretization(ds=0.004)
cylinder = section.extrusion(limits=(0.0, 3.2), ds=0.04)
cylinder.write(file_path='flyingSnake3dAoA35.body')
