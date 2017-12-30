"""
Plots and saves the z-component of the 3D vorticity field at given states.

CLI: visit -cli -s <script-path>
"""

import os
import argparse


# Check version of VisIt
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


# Parse the command-line arguments
parser_formatter_class = argparse.ArgumentDefaultsHelpFormatter
parser_description = 'Plots the z-component of the vorticity field with VisIt.'
parser = argparse.ArgumentParser(description=parser_description,
                                 formatter_class=parser_formatter_class)
parser.add_argument('--host', '-host',
                    dest='host',
                    default='localhost',
                    help='Host name where data are saved.')
parser.add_argument('--directory', '-d',
                    dest='directory',
                    required=True,
                    help='Directory where data are saved.')
parser.add_argument('--out', '-o',
                    dest='out_directory',
                    default=os.getcwd(),
                    help='Local directory where to save the figures.')
parser.add_argument('--prefix', '-p',
                    dest='out_prefix',
                    default='wz_wx_wake3d_2k35_meshA_',
                    help='Prefix to use for output file names.')
makemovie_path = '/usr/local/visit/2.12.1/linux-x86_64/bin/makemovie.py'
parser.add_argument('--makemovie', '-makemovie',
                    dest='makemovie',
                    default=makemovie_path,
                    help='Path of the VisIt script makemovie.py.')
args = parser.parse_args()


if not os.path.isdir(args.out_directory):
  raise NameError('Directory {} does not exist; please create it.'
                  .format(args.out_directory))

# Open the file with the coordinates of the immersed boundary
filepath = os.path.join(args.directory, 'flyingSnake3dAoA35.txt')
OpenDatabase('{}:{}'.format(args.host, filepath), 0, 'Point3D_1.0')

# Plot the mesh points
AddPlot('Mesh', 'points', 1, 1)

MeshAtts = MeshAttributes()
MeshAtts.legendFlag = 0
MeshAtts.lineStyle = MeshAtts.SOLID
MeshAtts.lineWidth = 0
MeshAtts.meshColor = (255, 204, 0, 255)
MeshAtts.meshColorSource = MeshAtts.MeshCustom
MeshAtts.opaqueColorSource = MeshAtts.Background
MeshAtts.opaqueMode = MeshAtts.Auto
MeshAtts.pointSize = 0.05
MeshAtts.opaqueColor = (255, 255, 255, 255)
MeshAtts.smoothingLevel = MeshAtts.None
MeshAtts.pointSizeVarEnabled = 0
MeshAtts.pointSizeVar = 'default'
MeshAtts.pointType = MeshAtts.Point
MeshAtts.showInternal = 0
MeshAtts.pointSizePixels = 2
MeshAtts.opacity = 1

SetPlotOptions(MeshAtts)

# Open the XMF file for the z-component of the vorticity field
filepath = os.path.join(args.directory, 'wz.xmf')
OpenDatabase('{}:{}'.format(args.host, filepath), 0)

# Plot the contour of the z-component of the vorticity field
AddPlot('Contour', 'wz', 1, 1)

ContourAtts = ContourAttributes()
ContourAtts.defaultPalette.GetControlPoints(0).colors = (255, 0, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(0).position = 0
ContourAtts.defaultPalette.GetControlPoints(1).colors = (0, 255, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(1).position = 0.034
ContourAtts.defaultPalette.GetControlPoints(2).colors = (0, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(2).position = 0.069
ContourAtts.defaultPalette.GetControlPoints(3).colors = (0, 255, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(3).position = 0.103
ContourAtts.defaultPalette.GetControlPoints(4).colors = (255, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(4).position = 0.138
ContourAtts.defaultPalette.GetControlPoints(5).colors = (255, 255, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(5).position = 0.172
ContourAtts.defaultPalette.GetControlPoints(6).colors = (255, 135, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(6).position = 0.207
ContourAtts.defaultPalette.GetControlPoints(7).colors = (255, 0, 135, 255)
ContourAtts.defaultPalette.GetControlPoints(7).position = 0.241
ContourAtts.defaultPalette.GetControlPoints(8).colors = (168, 168, 168, 255)
ContourAtts.defaultPalette.GetControlPoints(8).position = 0.276
ContourAtts.defaultPalette.GetControlPoints(9).colors = (255, 68, 68, 255)
ContourAtts.defaultPalette.GetControlPoints(9).position = 0.31
ContourAtts.defaultPalette.GetControlPoints(10).colors = (99, 255, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(10).position = 0.345
ContourAtts.defaultPalette.GetControlPoints(11).colors = (99, 99, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(11).position = 0.379
ContourAtts.defaultPalette.GetControlPoints(12).colors = (40, 165, 165, 255)
ContourAtts.defaultPalette.GetControlPoints(12).position = 0.414
ContourAtts.defaultPalette.GetControlPoints(13).colors = (255, 99, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(13).position = 0.448
ContourAtts.defaultPalette.GetControlPoints(14).colors = (255, 255, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(14).position = 0.483
ContourAtts.defaultPalette.GetControlPoints(15).colors = (255, 170, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(15).position = 0.517
ContourAtts.defaultPalette.GetControlPoints(16).colors = (170, 79, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(16).position = 0.552
ContourAtts.defaultPalette.GetControlPoints(17).colors = (150, 0, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(17).position = 0.586
ContourAtts.defaultPalette.GetControlPoints(18).colors = (0, 150, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(18).position = 0.621
ContourAtts.defaultPalette.GetControlPoints(19).colors = (0, 0, 150, 255)
ContourAtts.defaultPalette.GetControlPoints(19).position = 0.655
ContourAtts.defaultPalette.GetControlPoints(20).colors = (0, 109, 109, 255)
ContourAtts.defaultPalette.GetControlPoints(20).position = 0.69
ContourAtts.defaultPalette.GetControlPoints(21).colors = (150, 0, 150, 255)
ContourAtts.defaultPalette.GetControlPoints(21).position = 0.724
ContourAtts.defaultPalette.GetControlPoints(22).colors = (150, 150, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(22).position = 0.759
ContourAtts.defaultPalette.GetControlPoints(23).colors = (150, 84, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(23).position = 0.793
ContourAtts.defaultPalette.GetControlPoints(24).colors = (160, 0, 79, 255)
ContourAtts.defaultPalette.GetControlPoints(24).position = 0.828
ContourAtts.defaultPalette.GetControlPoints(25).colors = (255, 104, 28, 255)
ContourAtts.defaultPalette.GetControlPoints(25).position = 0.862
ContourAtts.defaultPalette.GetControlPoints(26).colors = (0, 170, 81, 255)
ContourAtts.defaultPalette.GetControlPoints(26).position = 0.897
ContourAtts.defaultPalette.GetControlPoints(27).colors = (68, 255, 124, 255)
ContourAtts.defaultPalette.GetControlPoints(27).position = 0.931
ContourAtts.defaultPalette.GetControlPoints(28).colors = (0, 130, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(28).position = 0.966
ContourAtts.defaultPalette.GetControlPoints(29).colors = (130, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(29).position = 1
ContourAtts.defaultPalette.smoothing = ContourAtts.defaultPalette.None
ContourAtts.defaultPalette.equalSpacingFlag = 1
ContourAtts.defaultPalette.discreteFlag = 1
ContourAtts.defaultPalette.categoryName = 'Standard'
ContourAtts.changedColors = (0, 1)
ContourAtts.colorType = ContourAtts.ColorByMultipleColors
ContourAtts.colorTableName = 'Default'
ContourAtts.invertColorTable = 0
ContourAtts.legendFlag = 1
ContourAtts.lineStyle = ContourAtts.SOLID
ContourAtts.lineWidth = 0
ContourAtts.singleColor = (255, 0, 0, 255)
ContourAtts.SetMultiColor(0, (0, 51, 102, 155))
ContourAtts.SetMultiColor(1, (255, 0, 0, 155))
ContourAtts.contourNLevels = 2
ContourAtts.contourValue = ()
ContourAtts.contourPercent = ()
ContourAtts.contourMethod = ContourAtts.Level
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -5.0
ContourAtts.max = 5.0
ContourAtts.scaling = ContourAtts.Linear
ContourAtts.wireframe = 0
SetPlotOptions(ContourAtts)

# Open the XMF file for the z-component of the vorticity field
filepath = os.path.join(args.directory, 'wx.xmf')
OpenDatabase('{}:{}'.format(args.host, filepath), 0)

# Plot the contour of the z-component of the vorticity field
AddPlot('Contour', 'wx', 1, 1)

ContourAtts = ContourAttributes()
ContourAtts.defaultPalette.GetControlPoints(0).colors = (255, 0, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(0).position = 0
ContourAtts.defaultPalette.GetControlPoints(1).colors = (0, 255, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(1).position = 0.034
ContourAtts.defaultPalette.GetControlPoints(2).colors = (0, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(2).position = 0.069
ContourAtts.defaultPalette.GetControlPoints(3).colors = (0, 255, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(3).position = 0.103
ContourAtts.defaultPalette.GetControlPoints(4).colors = (255, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(4).position = 0.138
ContourAtts.defaultPalette.GetControlPoints(5).colors = (255, 255, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(5).position = 0.172
ContourAtts.defaultPalette.GetControlPoints(6).colors = (255, 135, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(6).position = 0.207
ContourAtts.defaultPalette.GetControlPoints(7).colors = (255, 0, 135, 255)
ContourAtts.defaultPalette.GetControlPoints(7).position = 0.241
ContourAtts.defaultPalette.GetControlPoints(8).colors = (168, 168, 168, 255)
ContourAtts.defaultPalette.GetControlPoints(8).position = 0.276
ContourAtts.defaultPalette.GetControlPoints(9).colors = (255, 68, 68, 255)
ContourAtts.defaultPalette.GetControlPoints(9).position = 0.31
ContourAtts.defaultPalette.GetControlPoints(10).colors = (99, 255, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(10).position = 0.345
ContourAtts.defaultPalette.GetControlPoints(11).colors = (99, 99, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(11).position = 0.379
ContourAtts.defaultPalette.GetControlPoints(12).colors = (40, 165, 165, 255)
ContourAtts.defaultPalette.GetControlPoints(12).position = 0.414
ContourAtts.defaultPalette.GetControlPoints(13).colors = (255, 99, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(13).position = 0.448
ContourAtts.defaultPalette.GetControlPoints(14).colors = (255, 255, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(14).position = 0.483
ContourAtts.defaultPalette.GetControlPoints(15).colors = (255, 170, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(15).position = 0.517
ContourAtts.defaultPalette.GetControlPoints(16).colors = (170, 79, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(16).position = 0.552
ContourAtts.defaultPalette.GetControlPoints(17).colors = (150, 0, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(17).position = 0.586
ContourAtts.defaultPalette.GetControlPoints(18).colors = (0, 150, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(18).position = 0.621
ContourAtts.defaultPalette.GetControlPoints(19).colors = (0, 0, 150, 255)
ContourAtts.defaultPalette.GetControlPoints(19).position = 0.655
ContourAtts.defaultPalette.GetControlPoints(20).colors = (0, 109, 109, 255)
ContourAtts.defaultPalette.GetControlPoints(20).position = 0.69
ContourAtts.defaultPalette.GetControlPoints(21).colors = (150, 0, 150, 255)
ContourAtts.defaultPalette.GetControlPoints(21).position = 0.724
ContourAtts.defaultPalette.GetControlPoints(22).colors = (150, 150, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(22).position = 0.759
ContourAtts.defaultPalette.GetControlPoints(23).colors = (150, 84, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(23).position = 0.793
ContourAtts.defaultPalette.GetControlPoints(24).colors = (160, 0, 79, 255)
ContourAtts.defaultPalette.GetControlPoints(24).position = 0.828
ContourAtts.defaultPalette.GetControlPoints(25).colors = (255, 104, 28, 255)
ContourAtts.defaultPalette.GetControlPoints(25).position = 0.862
ContourAtts.defaultPalette.GetControlPoints(26).colors = (0, 170, 81, 255)
ContourAtts.defaultPalette.GetControlPoints(26).position = 0.897
ContourAtts.defaultPalette.GetControlPoints(27).colors = (68, 255, 124, 255)
ContourAtts.defaultPalette.GetControlPoints(27).position = 0.931
ContourAtts.defaultPalette.GetControlPoints(28).colors = (0, 130, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(28).position = 0.966
ContourAtts.defaultPalette.GetControlPoints(29).colors = (130, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(29).position = 1
ContourAtts.defaultPalette.smoothing = ContourAtts.defaultPalette.None
ContourAtts.defaultPalette.equalSpacingFlag = 1
ContourAtts.defaultPalette.discreteFlag = 1
ContourAtts.defaultPalette.categoryName = 'Standard'
ContourAtts.changedColors = (0, 1)
ContourAtts.colorType = ContourAtts.ColorByMultipleColors
ContourAtts.colorTableName = 'Default'
ContourAtts.invertColorTable = 0
ContourAtts.legendFlag = 1
ContourAtts.lineStyle = ContourAtts.SOLID
ContourAtts.lineWidth = 0
ContourAtts.singleColor = (255, 0, 0, 255)
ContourAtts.SetMultiColor(0, (51, 51, 51, 155))
ContourAtts.SetMultiColor(1, (255, 102, 0, 155))
ContourAtts.contourNLevels = 2
ContourAtts.contourValue = ()
ContourAtts.contourPercent = ()
ContourAtts.contourMethod = ContourAtts.Level
ContourAtts.minFlag = 1
ContourAtts.maxFlag = 1
ContourAtts.min = -20.0
ContourAtts.max = 20.0
ContourAtts.scaling = ContourAtts.Linear
ContourAtts.wireframe = 0
SetPlotOptions(ContourAtts)

DrawPlots()

# Set the view
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

SetActiveWindow(1)

Source(args.makemovie)
ToggleCameraViewMode()

# Loop over the states to render and save the plots
states = list(range(0, TimeSliderGetNStates(), 1))
for state in states:
  print('[state {}] Rendering and saving figure ...'.format(state))
  SetTimeSliderState(state)

  RenderingAtts = RenderingAttributes()
  RenderingAtts.antialiasing = 0
  RenderingAtts.orderComposite = 1
  RenderingAtts.depthCompositeThreads = 2
  RenderingAtts.depthCompositeBlocking = 65536
  RenderingAtts.alphaCompositeThreads = 2
  RenderingAtts.alphaCompositeBlocking = 65536
  RenderingAtts.depthPeeling = 0
  RenderingAtts.occlusionRatio = 0
  RenderingAtts.numberOfPeels = 16
  RenderingAtts.multiresolutionMode = 0
  RenderingAtts.multiresolutionCellSize = 0.002
  RenderingAtts.geometryRepresentation = RenderingAtts.Surfaces
  RenderingAtts.displayListMode = RenderingAtts.Auto
  RenderingAtts.stereoRendering = 0
  RenderingAtts.stereoType = RenderingAtts.CrystalEyes
  RenderingAtts.notifyForEachRender = 0
  RenderingAtts.scalableActivationMode = RenderingAtts.Auto
  RenderingAtts.scalableAutoThreshold = 2000000
  RenderingAtts.specularFlag = 0
  RenderingAtts.specularCoeff = 0.6
  RenderingAtts.specularPower = 10
  RenderingAtts.specularColor = (255, 255, 255, 255)
  RenderingAtts.doShadowing = 0
  RenderingAtts.shadowStrength = 0.5
  RenderingAtts.doDepthCueing = 0
  RenderingAtts.depthCueingAutomatic = 1
  RenderingAtts.startCuePoint = (-10, 0, 0)
  RenderingAtts.endCuePoint = (10, 0, 0)
  RenderingAtts.compressionActivationMode = RenderingAtts.Never
  RenderingAtts.colorTexturingFlag = 1
  RenderingAtts.compactDomainsActivationMode = RenderingAtts.Never
  RenderingAtts.compactDomainsAutoThreshold = 256
  SetRenderingAttributes(RenderingAtts)

  SaveWindowAtts = SaveWindowAttributes()
  SaveWindowAtts.outputToCurrentDirectory = 0
  SaveWindowAtts.outputDirectory = args.out_directory
  SaveWindowAtts.fileName = '{}{:0>4}'.format(args.out_prefix, state)
  SaveWindowAtts.family = 0
  SaveWindowAtts.format = SaveWindowAtts.PNG
  SaveWindowAtts.width = 1045
  SaveWindowAtts.height = 956
  SaveWindowAtts.screenCapture = 0
  SaveWindowAtts.saveTiled = 0
  SaveWindowAtts.quality = 80
  SaveWindowAtts.progressive = 0
  SaveWindowAtts.binary = 0
  SaveWindowAtts.stereo = 0
  SaveWindowAtts.compression = SaveWindowAtts.PackBits
  SaveWindowAtts.forceMerge = 0
  SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
  SaveWindowAtts.advancedMultiWindowSave = 0
  SetSaveWindowAttributes(SaveWindowAtts)

  SaveWindow()

exit(0)
