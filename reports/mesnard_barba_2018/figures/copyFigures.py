"""
Copy figures (to be added in the paper) into the present directory.
"""

import os
import shutil


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.sep.join(script_dir.split(os.sep)[:-3])
figures_dir = script_dir

filename = 'latencyBandwidthColonialOneAzure.png'
filepath = os.path.join(root_dir, 'runs', 'figures', filename)
shutil.copy(filepath, figures_dir)

filename = 'poissonScalingColonialOneAzureA9.png'
filepath = os.path.join(root_dir, 'runs', 'figures', filename)
shutil.copy(filepath, figures_dir)
