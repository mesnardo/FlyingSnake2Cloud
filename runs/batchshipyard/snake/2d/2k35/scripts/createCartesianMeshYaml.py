"""
Creates a YAML file with info about the structured Cartesian mesh that will be
parsed by PetIBM.

Creates a 2D structured Cartesian grid.
"""

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
mesh.create(info, mode='cuibm')
mesh.print_parameters()
mesh.write_yaml_file('cartesianMesh.yaml')
