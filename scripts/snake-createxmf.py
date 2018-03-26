#!/usr/bin/env python
"""
Creates an XMF file for the x-component of the velocity field.
"""

import sys
import argparse
import pathlib
from lxml import etree


if sys.version_info < (3, 4):
  raise ImportError('Python 3.4+ is supported.')

# Parse command-line arguments
parser_formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser_description = 'Create XMF file for components sharing the same grid.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--version', '-V',
                    action='version',
                    version='%(prog)s (version 0.1)')

parser.add_argument('--grid-path', '-g',
                    dest='grid_path', type=str, required=True,
                    help='Path of the grid file.')
parser.add_argument('--grid-size', '-s',
                    dest='grid_size', type=int, nargs='+',
                    help='Grid size: nx followed by ny (and nz if 3D).')
parser.add_argument('--data-dir', '-d',
                    dest='data_dir', type=str, required=True,
                    help='Directory containing the numerical solution.')
parser.add_argument('--variables', '-v',
                    dest='variables', type=str, nargs='+',
                    help='Variable names that shares the same grid.')
parser.add_argument('--start',
                    dest='start', type=int, default=None,
                    help='Starting state to consider.')
parser.add_argument('--end',
                    dest='end', type=int, default=None,
                    help='Ending state to consider.')
parser.add_argument('--step',
                    dest='step', type=int, default=None,
                    help='Number of steps between two states.')
parser.add_argument('--dt',
                    dest='dt', type=float, required=True,
                    help='Time increment.')
parser.add_argument('--output', '-o',
                    dest='output', type=str,
                    default=pathlib.Path() / 'var.xmf',
                    help='Path of XMF output file.')
args = parser.parse_args()

# Convert string into absolute pathlib.Path
for name in ['data_dir', 'grid_path', 'output']:
  setattr(args, name, pathlib.Path(getattr(args, name)).resolve())

# Start XMF tree
xdmf = etree.Element('Xdmf', Version='2.2')
info = etree.SubElement(xdmf, 'Information', Name='MetaData', Value='ID-23454')
domain = etree.SubElement(xdmf, 'Domain')
grid_time_series = etree.SubElement(domain, 'Grid',
                                    Name='TimeSeries',
                                    GridType='Collection',
                                    CollectionType='Temporal')

# Define type of field
dim = len(args.grid_size)
if dim == 2:
  topology_type = '2DRectMesh'
  geometry_type = 'VXVY'
  components = ('x', 'y')
elif dim == 3:
  topology_type = '3DRectMesh'
  geometry_type = 'VXVYVZ'
  components = ('x', 'y', 'z')
number_of_elements = ' '.join(str(n) for n in args.grid_size[::-1])
precision = '8'

# Create an XMF block for each time-step saved
states = [i for i in range(args.start, args.end + 1, args.step)]
times = [state * args.dt for state in states]
for state, time in zip(states, times):
  grid = etree.SubElement(grid_time_series, 'Grid',
                          Name='Grid',
                          GridType='Uniform')
  time = etree.SubElement(grid, 'Time', Value=str(time))
  topology = etree.SubElement(grid, 'Topology',
                              TopologyType=topology_type,
                              NumberOfElements=number_of_elements)
  geometry = etree.SubElement(grid, 'Geometry', GeometryType=geometry_type)

  # Loop over the 3 directions (for code-reuse purpose)
  for component, n in zip(components, args.grid_size):
    dataitem = etree.SubElement(geometry, 'DataItem',
                                Dimensions=str(n),
                                NumberType='Float',
                                Precision=precision,
                                Format='HDF')
    dataitem.text = ':/'.join([str(args.grid_path), component])

  # Create a block for each variable to insert
  for variable in args.variables:
    attribute = etree.SubElement(grid, 'Attribute',
                                 Name=variable,
                                 AttributeType='Scalar',
                                 Center='Node')
    dataitem = etree.SubElement(attribute, 'DataItem',
                                Dimensions=number_of_elements,
                                NumberType='Float',
                                Precision=precision,
                                Format='HDF')
    variable_filepath = args.data_dir / '{:0>7}/{}.h5'.format(state, variable)
    dataitem.text = ':/'.join([str(variable_filepath), variable])

# Write the XMF file
args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
tree = etree.ElementTree(xdmf)
tree.write(str(args.output), pretty_print=True, xml_declaration=True)
