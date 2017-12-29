"""
Plots the vorticity field at saved time-steps using the visualization software
VisIt.

CLI: visit -nowin -cli -s scripts/plotVorticity.py
"""

import os
import math


def recorded_views(label):
  """
  Get the dimensions of the view from recorded ones.

  Parameters
  ----------
  label: string
    Dictionary key for the view.

  Returns
  -------
  view: 4-tuple of floats
    The view ('xmin', 'xmax', 'ymin', 'ymax').
  """
  views = {}
  views['snake'] = (-1.0, 2.0, -1.5, 1.5)
  views['wake'] = (-1.0, 15.0, -4.0, 4.0)
  views['domain'] = (-15.0, 15.0, -15.0, 15.0)
  views['default'] = (-1.0, 1.0, -1.0, 1.0)
  if label not in views.keys():
    label = 'default'
  return views[label]


def check_version():
  """
  Check the VisIt version and prints warning if the version has not been
  tested.
  """
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


check_version()

# User's configuration
config = {}
script_dir = os.path.dirname(os.path.realpath(__file__))
config['directory'] = os.path.abspath(os.path.join(script_dir, os.pardir))
config['file name'] = 'wz.xmf'
OpenDatabase('{}:{}'.format(GetLocalHostName(),
                            os.path.join(config['directory'],
                                         config['file name'])),
             0)
config['name'] = 'wz'
config['type'] = 'Pseudocolor'
config['range'] = (-5.0, 5.0)
config['view label'] = 'wake'
config['view'] = recorded_views(config['view label'])
config['color table name'] = 'viridis'
config['invert color table'] = False
config['states range'] = (0, TimeSliderGetNStates(), 1)
config['figure width'] = 800
view_string = '_'.join(['{:.2f}'.format(v) for v in config['view']])
config['output directory'] = os.path.join(config['directory'],
                                          'figures',
                                          '_'.join([config['name'],
                                                    view_string]))
# End of user's configuration

HideActivePlots()
AddPlot(config['type'], config['name'], 1, 1)
DrawPlots()

# legend settings
legend = GetAnnotationObject(GetPlotList().GetPlots(0).plotName)
if config['view label'] == 'snake':
  legend.xScale = 2.0
  legend.yScale = 0.25
  legend.numberFormat = '%# -9.2g'
  legend.orientation = legend.HorizontalBottom
  legend.managePosition = 0
  legend.position = (0.10, 0.10)
  legend.fontFamily = legend.Courier
  legend.fontBold = 0
  legend.fontHeight = 0.1
  legend.drawMinMax = 0
  legend.drawTitle = 0
elif config['view label'] == 'wake':
  legend.xScale = 1.5
  legend.yScale = 0.5
  legend.numberFormat = '%# -9.2g'
  legend.orientation = legend.HorizontalBottom
  legend.managePosition = 0
  legend.position = (0.10, 0.10)
  legend.fontFamily = legend.Courier
  legend.fontBold = 0
  legend.fontHeight = 0.1
  legend.drawMinMax = 0
  legend.drawTitle = 0
elif config['view label'] == 'domain':
  legend.xScale = 1.5
  legend.yScale = 0.25
  legend.numberFormat = '%# -9.2g'
  legend.orientation = legend.HorizontalBottom
  legend.managePosition = 0
  legend.position = (0.10, 0.10)
  legend.fontFamily = legend.Courier
  legend.fontBold = 0
  legend.fontHeight = 0.1
  legend.drawMinMax = 0
  legend.drawTitle = 0

# create time-annotation
time_annotation = CreateAnnotationObject('Text2D')
if config['view label'] == 'snake':
  time_annotation.position = (0.05, 0.90)
  time_annotation.fontFamily = 1
  time_annotation.fontBold = 0
  time_annotation.height = 0.025
elif config['view label'] == 'wake':
  time_annotation.position = (0.05, 0.90)
  time_annotation.fontFamily = 1
  time_annotation.fontBold = 0
  time_annotation.height = 0.05
elif config['view label'] == 'domain':
  time_annotation.position = (0.05, 0.90)
  time_annotation.fontFamily = 1
  time_annotation.fontBold = 0
  time_annotation.height = 0.04

# define size of the figure in pixels
ratio = ((config['view'][3] - config['view'][2]) /
         (config['view'][1] - config['view'][0]))
config['figure height'] = int(math.floor(config['figure width'] * ratio))
# define and create figures directory
if not os.path.isdir(config['output directory']):
  print('[info] Create output directory {}'.format(config['output directory']))
  os.makedirs(config['output directory'])

PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = config['range'][0]
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = config['range'][1]
PseudocolorAtts.centering = PseudocolorAtts.Natural
PseudocolorAtts.colorTableName = config['color table name']
PseudocolorAtts.invertColorTable = config['invert color table']
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque
PseudocolorAtts.opacityVariable = ''
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = 'default'
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID
PseudocolorAtts.lineType = PseudocolorAtts.Line
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ''
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None
PseudocolorAtts.headStyle = PseudocolorAtts.None
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ''
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)

View2DAtts = View2DAttributes()
View2DAtts.windowCoords = config['view']
View2DAtts.viewportCoords = (0, 1, 0, 1)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR
View2DAtts.yScale = View2DAtts.LINEAR
View2DAtts.windowValid = 1
SetView2D(View2DAtts)

AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.visible = 1
AnnotationAtts.axes2D.autoSetTicks = 1
AnnotationAtts.axes2D.autoSetScaling = 1
AnnotationAtts.axes2D.lineWidth = 0
AnnotationAtts.axes2D.tickLocation = AnnotationAtts.axes2D.Inside
AnnotationAtts.axes2D.tickAxes = AnnotationAtts.axes2D.BottomLeft
# x-axis
AnnotationAtts.axes2D.xAxis.title.visible = 0
AnnotationAtts.axes2D.xAxis.label.visible = 0
AnnotationAtts.axes2D.xAxis.tickMarks.visible = 0
AnnotationAtts.axes2D.xAxis.grid = 0
# y-axis
AnnotationAtts.axes2D.yAxis.title.visible = 0
AnnotationAtts.axes2D.yAxis.label.visible = 0
AnnotationAtts.axes2D.yAxis.tickMarks.visible = 0
AnnotationAtts.axes2D.yAxis.grid = 0
# user's name
AnnotationAtts.userInfoFlag = 0
# settings for legend
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
AnnotationAtts.legendInfoFlag = 1
AnnotationAtts.backgroundColor = (255, 255, 255, 255)
AnnotationAtts.foregroundColor = (0, 0, 0, 255)
AnnotationAtts.gradientBackgroundStyle = AnnotationAtts.Radial
AnnotationAtts.gradientColor1 = (0, 0, 255, 255)
AnnotationAtts.gradientColor2 = (0, 0, 0, 255)
AnnotationAtts.backgroundMode = AnnotationAtts.Solid
AnnotationAtts.backgroundImage = ''
AnnotationAtts.imageRepeatX = 1
AnnotationAtts.imageRepeatY = 1
AnnotationAtts.axesArray.visible = 0
SetAnnotationAttributes(AnnotationAtts)

if 'states' in config.keys():
  states = config['states']
else:
  states = range(*config['states range'])

for state in states:
  SetTimeSliderState(state)
  time = float(Query('Time')[:-1].split()[-1])
  print('\n[state {}] Time: {} - Create and save field.'
        ''.format(state, time))

  time_annotation.text = 'Time: {0:.3f}'.format(time)

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
  SaveWindowAtts.outputDirectory = config['output directory']
  SaveWindowAtts.fileName = '{}{:0>7}'.format(config['name'], state)
  SaveWindowAtts.family = 0
  SaveWindowAtts.format = SaveWindowAtts.PNG
  SaveWindowAtts.width = config['figure width']
  SaveWindowAtts.height = config['figure height']
  SaveWindowAtts.screenCapture = 0
  SaveWindowAtts.saveTiled = 0
  SaveWindowAtts.quality = 100
  SaveWindowAtts.progressive = 0
  SaveWindowAtts.binary = 0
  SaveWindowAtts.stereo = 0
  SaveWindowAtts.compression = SaveWindowAtts.PackBits
  SaveWindowAtts.forceMerge = 0
  SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
  SaveWindowAtts.advancedMultiWindowSave = 0
  SetSaveWindowAttributes(SaveWindowAtts)

  SaveWindow()

os.remove('visitlog.py')
exit(0)
