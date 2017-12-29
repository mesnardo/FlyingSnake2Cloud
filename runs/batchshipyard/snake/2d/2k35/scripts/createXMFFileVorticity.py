"""
Creates an XMF file for variables that share the same grid.
  """

import os
from lxml import etree as ET
import numpy


# User's configuration
config = {}
script_dir = os.path.dirname(os.path.realpath(__file__))
config['directory'] = os.path.abspath(os.path.join(script_dir, os.pardir))
config['grid file'] = os.path.join(config['directory'], 'grids', 'wz.h5')
config['grid size'] = (1703, 1703)
config['variables'] = ['wz']
config['states range'] = (2500, 200000 + 1, 2500)
config['time step size'] = 4.0E-04
config['output'] = os.path.join(config['directory'], 'wz.xmf')
# End of user's configuration

# get list of states
states = numpy.arange(*config['states range'])
times = config['time step size'] * states

# start xmf tree
xdmf = ET.Element('Xdmf',
                  Version='2.2')
info = ET.SubElement(xdmf, 'Information',
                     Name='MetaData',
                     Value='ID-23454')
domain = ET.SubElement(xdmf, 'Domain')
grid_time_series = ET.SubElement(domain, 'Grid',
                                 Name='TimeSeries',
                                 GridType='Collection',
                                 CollectionType='Temporal')
# define type of field
if len(config['grid size']) == 2:
  topology_type = '2DRectMesh'
  geometry_type = 'VXVY'
  components = ('x', 'y')
elif len(config['grid size']) == 3:
  topology_type = '3DRectMesh'
  geometry_type = 'VXVYVZ'
  components = ('x', 'y', 'z')
number_of_elements = ' '.join(str(n) for n in config['grid size'][::-1])
precision = '8'

# create an xmf block for each time-step saved
for state, time in zip(states, times):
  grid = ET.SubElement(grid_time_series, 'Grid',
                       Name='Grid',
                       GridType='Uniform')
  time = ET.SubElement(grid, 'Time',
                       Value=str(time))
  topology = ET.SubElement(grid, 'Topology',
                           TopologyType=topology_type,
                           NumberOfElements=number_of_elements)
  geometry = ET.SubElement(grid, 'Geometry',
                           GeometryType=geometry_type)
  # loop over the 3 directions (for code-reuse purpose)
  for component, n in zip(components, config['grid size']):
    dataitem = ET.SubElement(geometry, 'DataItem',
                             Dimensions=str(n),
                             NumberType='Float',
                             Precision=precision,
                             Format='HDF')
    dataitem.text = '{}:/{}'.format(os.path.join(config['directory'],
                                                 config['grid file']),
                                    component)
  # create a block for each variable to insert
  for variable in config['variables']:
    attribute = ET.SubElement(grid, 'Attribute',
                              Name=variable,
                              AttributeType='Scalar',
                              Center='Node')
    dataitem = ET.SubElement(attribute, 'DataItem',
                             Dimensions=number_of_elements,
                             NumberType='Float',
                             Precision=precision,
                             Format='HDF')
    variable_file_path = os.path.join(config['directory'],
                                      '{:0>7}'.format(state),
                                      '{}.h5'.format(variable))
    dataitem.text = '{}:/{}'.format(variable_file_path, variable)
# write the xmf file
tree = ET.ElementTree(xdmf)
tree.write(config['output'], pretty_print=True, xml_declaration=True)
