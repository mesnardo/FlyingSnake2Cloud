"""
Creates a YAML file with info about the structured Cartesian mesh that will be
parsed by PetIBM.

Creates a 3D structured Cartesian grid.
"""

import pathlib
import math
from snake.cartesianMesh import CartesianStructuredMesh


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent

# info about the 3D structured Cartesian grid
width = 0.008  # minimum grid spacing in the x- and y- directions
chord = 1.0  # chord-length of the body cross-section
spanwise_width = 10.0 * width  # grid-spacing in the spanwise direction
spanwise_length = 3.2 * chord  # target spanwise length
spanwise_cells = math.ceil(spanwise_length / spanwise_width)  # cells required
spanwise_length = spanwise_cells * spanwise_width  # actual spanwise length
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
                         'precision': 2}]},
        {'direction': 'z', 'start': 0.0,
         'subDomains': [{'end': spanwise_length,
                         'width': spanwise_width,
                         'stretchRatio': 1.0}]}]

mesh = CartesianStructuredMesh()
mesh.create(info)
mesh.print_parameters()
filepath = root_dir / 'cartesianMesh.yaml'
mesh.write_yaml_file(str(filepath))
