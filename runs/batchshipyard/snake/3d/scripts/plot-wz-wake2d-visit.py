"""
Plots and saves a slice of the z-component of the 3D vorticity field
at given states.

CLI: visit -cli -s <script-path>
"""

import os
import argparse


# Check version of VisIt.
script_version = '2.12.1'
tested_versions = [script_version]
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
parser_description = 'Plots the z-component of the vorticity field with VisIt.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--directory', '-d',
                    dest='data_dir',
                    type=str,
                    required=True,
                    help='Directory where data are saved.')
parser.add_argument('--range',
                    dest='range',
                    nargs=3,
                    type=int,
                    default=[0, None, 1],
                    help='Range to plot (start, end, step).')
parser.add_argument('--out', '-o',
                    dest='out_dir',
                    type=str,
                    default=os.getcwd(),
                    help='Local directory where to save the figures.')
parser.add_argument('--out-prefix', '-p',
                    dest='out_prefix',
                    type=str,
                    default='wz_wake2d_',
                    help='Prefix to use for output file names.')
makemovie_path = '/usr/local/visit/2.12.1/linux-x86_64/bin/makemovie.py'
parser.add_argument('--makemovie', '-makemovie',
                    dest='makemovie',
                    type=str,
                    default=makemovie_path,
                    help='Path of the VisIt script makemovie.py.')
args = parser.parse_args()

# Create output directory if necessary.
if not os.path.isdir(args.out_dir):
  raise NameError('Directory {} does not exist; please create it.'
                  .format(args.out_dir))

# Create data correlation.
filenames = ['snake.obj', 'wz.xmf']
databases = [args.data_dir + '/' + name for name in filenames]
CreateDatabaseCorrelation('common', databases[1:], 0)

# Open the OBJ file with the coordinates of the immersed boundary.
OpenDatabase(databases[0], 0)
# Add plot the mesh points.
AddPlot('Mesh', 'OBJMesh', 1, 1)
# Set attributes of the mesh plot.
MeshAtts = MeshAttributes()
MeshAtts.legendFlag = 0
MeshAtts.lineWidth = 1
MeshAtts.meshColorSource = MeshAtts.MeshCustom
SetPlotOptions(MeshAtts)

# Open the XMF file for the z-component of the vorticity.
OpenDatabase(databases[1], 0)
# Add the plot of the contour of the z-component of the vorticity.
AddPlot('Contour', 'wz', 1, 1)
# Set attributes of the contour.
ContourAtts = ContourAttributes()
ContourAtts.contourNLevels = 2
ContourAtts.SetMultiColor(0, (0, 51, 102, 1.0 * 255))
ContourAtts.SetMultiColor(1, (255, 0, 0, 1.0 * 255))
ContourAtts.legendFlag = 1
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -5.0
ContourAtts.max = 5.0
SetPlotOptions(ContourAtts)

# Create a 2D slice.
AddOperator('Slice', 1)
SetActivePlots((0, 1))
# Set attributes of the slice.
SliceAtts = SliceAttributes()
SliceAtts.originType = SliceAtts.Intercept
SliceAtts.originIntercept = 1.6
SliceAtts.normal = (0, 0, 1)
SliceAtts.axisType = SliceAtts.ZAxis
SliceAtts.upAxis = (0, 1, 0)
SliceAtts.meshName = 'OBJMesh'
SliceAtts.theta = 0
SliceAtts.phi = 90
SetOperatorOptions(SliceAtts, 1)

# Set the 2D view.
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (-1, 5, -2, 2)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.windowValid = 1
SetView2D(View2DAtts)

# Remove time and user info.
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
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

exit(0)
