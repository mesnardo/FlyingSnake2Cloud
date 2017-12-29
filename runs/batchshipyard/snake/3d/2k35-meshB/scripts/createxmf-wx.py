"""
Creates an XMF file for the x-component of the 3D vorticity field.
"""

import os
from lxml import etree as ET


# User's configuration
config = {}
script_dir = os.path.dirname(os.path.realpath(__file__))
simu_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
out_dir = os.path.join(simu_dir, 'postprocessing')
if not os.path.isdir(out_dir):
  os.makedirs(out_dir)
config['directory'] = out_dir
config['grid file'] = os.path.join(config['directory'],
                                   'grids', 'wx.h5')
config['grid size'] = (1704, 1705, 79)
config['variables'] = ['wx']
config['states'] = [100000, *(i for i in range(102400, 198400 + 1, 3200))]
config['time step size'] = 5.0E-04
config['time correction'] = 50.0
config['output'] = os.path.join(config['directory'], 'wx.xmf')
# End of user's configuration

# get list of states
states = config['states']
times = [config['time step size'] * state + config['time correction']
         for state in states]

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
