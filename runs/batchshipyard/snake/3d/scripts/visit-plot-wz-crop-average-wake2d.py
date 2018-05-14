"""
Plots and saves the spanwise-averaged z-component of the 3D vorticity field
at given states.

CLI: visit -cli -nowin -s <script-path>
"""

import sys
import os
import argparse


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
parser_description = 'Plots spanwise-averaged z-component of the vorticity.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--wz-xdmf-path',
                    dest='wz_xdmf_path',
                    type=str,
                    required=True,
                    help='Path of the XDMF file for the z-vorticity.')
parser.add_argument('--body-curve-path',
                    dest='body_curve_path',
                    type=str,
                    default=None,
                    help='Path of the curve file with 2D body coordinates.')
parser.add_argument('--range',
                    dest='range',
                    nargs=3,
                    type=int,
                    default=[0, None, 1],
                    help='Range to plot (start, end, step).')
parser.add_argument('--view',
                    dest='view',
                    nargs=4,
                    type=float,
                    default=None,
                    help='View (x-min, x-max, y-min, y-max).')
parser.add_argument('--out-dir',
                    dest='out_dir',
                    type=str,
                    default=os.getcwd(),
                    help='Local directory where to save the figures.')
parser.add_argument('--out-prefix',
                    dest='out_prefix',
                    type=str,
                    default='wz_average_wake2d_',
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
databases = [args.body_curve_path, args.wz_xdmf_path]
CreateDatabaseCorrelation('common', databases[1:], 0)

# Open the XMF file for the spanwise-averaged z-component of the vorticity.
OpenDatabase(databases[1], 0)
# Add pseudocolor of the spanwise-averaged z-component of the vorticity.
AddPlot('Pseudocolor', 'wz', 1, 1)
# Set attributes of the pseudocolor.
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -5
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 5
PseudocolorAtts.colorTableName = 'viridis'
SetPlotOptions(PseudocolorAtts)

# Open the curve file with the coordinates of the immersed boundary.
if databases[0]:
  OpenDatabase(databases[0], 0)
  # Add plot of the curve.
  AddPlot('Curve', 'curve', 1, 1)
  # Set attributes of the curve.
  CurveAtts = CurveAttributes()
  CurveAtts.lineWidth = 1
  CurveAtts.curveColorSource = CurveAtts.Custom  # Cycle, Custom
  CurveAtts.curveColor = (0, 0, 0, 255)
  CurveAtts.showLegend = 0
  CurveAtts.showLabels = 0
  SetPlotOptions(CurveAtts)

if args.view:
  # Set the 2D view.
  View2DAtts = View2DAttributes()
  View2DAtts.windowCoords = tuple(args.view)
  View2DAtts.viewportCoords = (0, 1, 0, 1)
  View2DAtts.fullFrameActivationMode = View2DAtts.Auto
  View2DAtts.fullFrameAutoThreshold = 100
  View2DAtts.xScale = View2DAtts.LINEAR
  View2DAtts.yScale = View2DAtts.LINEAR
  View2DAtts.windowValid = 1
  SetView2D(View2DAtts)

# Remove time and user info.
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.timeInfoFlag = 1
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
