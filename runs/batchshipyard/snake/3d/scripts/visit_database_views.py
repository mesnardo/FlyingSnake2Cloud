"""
List of predefined view attributes.
"""


def set_view3d_attributes(View3DAtts, name):
  if name == 'domain':
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
  elif name == 'crop':
    View3DAtts.viewNormal = (-0.31, 0.41, 0.86)
    View3DAtts.focus = (0, 0, 1.6)
    View3DAtts.viewUp = (0.24, 0.91, -0.34)
    View3DAtts.viewAngle = 30
    View3DAtts.parallelScale = 21
    View3DAtts.nearPlane = -42.1555
    View3DAtts.farPlane = 42.1555
    View3DAtts.imagePan = (0.06, -0.014)
    View3DAtts.imageZoom = 1.2
    View3DAtts.perspective = 1
    View3DAtts.eyeAngle = 2
    View3DAtts.centerOfRotationSet = 0
    View3DAtts.centerOfRotation = (0.0146802, 0, 1.6)
    View3DAtts.axis3DScaleFlag = 0
    View3DAtts.axis3DScales = (1, 1, 1)
    View3DAtts.shear = (0, 0, 1)
    View3DAtts.windowValid = 1
  return
