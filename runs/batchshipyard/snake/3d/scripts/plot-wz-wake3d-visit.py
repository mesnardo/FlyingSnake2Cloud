"""
Plots and saves the z-component of the 3D vorticity field
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
                    default='wz_wake3d_',
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
filenames = ['snake.p3d', 'wz.xmf']
databases = [args.data_dir + '/' + name for name in filenames]
CreateDatabaseCorrelation('common', databases[1:], 0)

# Open the file with the coordinates of the immersed boundary.
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

# Set attributes of the view.
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.31, 0.41, 0.86)
View3DAtts.focus = (0, 0, 1.6)
View3DAtts.viewUp = (0.24, 0.91, -0.34)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 21
View3DAtts.nearPlane = -42.1555
View3DAtts.farPlane = 42.1555
View3DAtts.imagePan = (-0.06, -0.014)
View3DAtts.imageZoom = 5.56
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (0.0146802, 0, 1.6)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)

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
