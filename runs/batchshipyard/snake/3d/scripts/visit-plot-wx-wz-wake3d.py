"""
Plots and saves the x- and z-components of the 3D vorticity field
at given states.

CLI: visit -cli -nowin -s <script-path>
"""

import sys
import os
import argparse
from visit_database_views import *


# Check version of VisIt.
script_version = '2.12.1'
tested_versions = [script_version, '2.12.3', '2.13.1']
current_version = Version()
print('VisIt version: {}\n'.format(Version()))
if current_version not in tested_versions:
  print('[warning] You are using VisIt-{}.'.format(current_version))
  print('[warning] This script was created with VisIt-{}.'
        .format(script_version))
  print('[warning] This script was tested with versions: {}.'
        .format(tested_versions))
  print('[warning] It may not work as expected')

# Parse the command-line arguments.
parser_formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser_description = ('Plots the x- and z-components of the vorticity field '
                      'with VisIt.')
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--wx-xdmf-path',
                    dest='wx_xdmf_path',
                    type=str,
                    required=True,
                    help='Path of the XDMF file for the x-vorticity.')
parser.add_argument('--wz-xdmf-path',
                    dest='wz_xdmf_path',
                    type=str,
                    required=True,
                    help='Path of the XDMF file for the z-vorticity.')
parser.add_argument('--body-p3d-path',
                    dest='body_p3d_path',
                    type=str,
                    default=None,
                    help='Path of the Point3D file with the body coordinates.')
parser.add_argument('--range',
                    dest='range',
                    nargs=3,
                    type=int,
                    default=[0, None, 1],
                    help='Range to plot (start, end, step).')
parser.add_argument('--view-name',
                    dest='view_name',
                    type=str,
                    default='domain',
                    help='Name of the View3DAttributes to load from database.')
parser.add_argument('--out-dir',
                    dest='out_dir',
                    type=str,
                    default=os.getcwd(),
                    help='Local directory where to save the figures.')
parser.add_argument('--out-prefix',
                    dest='out_prefix',
                    type=str,
                    default='wz_wx_wake3d_',
                    help='Prefix to use for output file names.')
parser.add_argument('--makemovie',
                    dest='makemovie',
                    type=str,
                    default=os.environ['MAKEMOVIE_PY'],
                    help='Path of the VisIt script makemovie.py.')
args = parser.parse_args()

# Create output directory if necessary.
if not os.path.isdir(args.out_dir):
  os.makedirs(args.out_dir)

# Create data correlation.
databases = [args.body_p3d_path, args.wz_xdmf_path, args.wx_xdmf_path]
CreateDatabaseCorrelation('common', databases[1:], 0)

# Open the file with the coordinates of the immersed boundary.
if databases[0]:
  OpenDatabase(databases[0], 0, 'Point3D_1.0')
  # Add plot the mesh points.
  AddPlot('Mesh', 'points', 1, 1)
  # Set attributes of the mesh plot.
  MeshAtts = MeshAttributes()
  MeshAtts.legendFlag = 0
  MeshAtts.meshColor = (255, 204, 0, 1.0 * 255)
  MeshAtts.meshColorSource = MeshAtts.MeshCustom
  MeshAtts.pointSize = 0.05
  MeshAtts.pointType = MeshAtts.Point
  MeshAtts.pointSizePixels = 2
  MeshAtts.opacity = 1
  SetPlotOptions(MeshAtts)

# Open the XMF file for the z-component of the vorticity.
OpenDatabase(databases[1], 0)
# Add the plot of the contour of the z-component of the vorticity.
AddPlot('Contour', 'wz', 1, 1)
# Set attributes of the contour.
ContourAtts = ContourAttributes()
ContourAtts.contourNLevels = 2
ContourAtts.SetMultiColor(0, (0, 51, 102, 0.6 * 255))
ContourAtts.SetMultiColor(1, (255, 0, 0, 0.6 * 255))
ContourAtts.legendFlag = 1
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -5.0
ContourAtts.max = 5.0
SetPlotOptions(ContourAtts)

# Open the XMF file for the x-component of the vorticity.
OpenDatabase(databases[2], 0)
# Add the plot of the contour of the x-component of the vorticity.
AddPlot('Contour', 'wx', 1, 1)
# Set attributes of the contour.
ContourAtts = ContourAttributes()
ContourAtts.contourNLevels = 2
ContourAtts.SetMultiColor(0, (51, 51, 51, 0.6 * 255))
ContourAtts.SetMultiColor(1, (255, 102, 0, 0.6 * 255))
ContourAtts.legendFlag = 1
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -20.0
ContourAtts.max = 20.0
SetPlotOptions(ContourAtts)

# Set attributes of the view.
View3DAtts = View3DAttributes()
set_view3d_attributes(View3DAtts, args.view_name)
SetView3D(View3DAtts)

# Remove time and user info.
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.axes3D.visible = 0
AnnotationAtts.axes3D.triadFlag = 1
AnnotationAtts.axes3D.bboxFlag = 0
SetAnnotationAttributes(AnnotationAtts)

DrawPlots()
SetActiveWindow(1)

Source(args.makemovie)
ToggleCameraViewMode()

# Loop over the states to render and save the plots.
if args.range[1] is None:
  args.range[1] = TimeSliderGetNStates()
else:
  args.range[1] += 1
for state in range(*args.range):
  print('[state {}] Rendering and saving figure ...'.format(state))
  SetTimeSliderState(state)

  RenderingAtts = RenderingAttributes()
  SetRenderingAttributes(RenderingAtts)

  SaveWindowAtts = SaveWindowAttributes()
  SaveWindowAtts.outputToCurrentDirectory = 0
  SaveWindowAtts.outputDirectory = args.out_dir
  SaveWindowAtts.fileName = '{}{:0>4}'.format(args.out_prefix, state)
  SaveWindowAtts.family = 0
  SaveWindowAtts.format = SaveWindowAtts.PNG
  SaveWindowAtts.width = 1024
  SaveWindowAtts.height = 1024
  SaveWindowAtts.quality = 100
  SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
  SetSaveWindowAttributes(SaveWindowAtts)

  SaveWindow()

sys.exit(0)
