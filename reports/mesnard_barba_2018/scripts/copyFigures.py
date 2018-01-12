"""
Copy figures (to be added in the paper) into the present directory.
"""

import os
import shutil

if not os.environ.get('AZ_SNAKE'):
  raise KeyError('Environment variable AZ_SNAKE is not set')

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.sep.join(script_dir.split(os.sep)[:-1])
root_dir = os.environ['AZ_SNAKE']
figures_dir = os.path.join(parent_dir, 'figures')

filename = 'latencyBandwidthColonialOneAzure.png'
filepath = os.path.join(root_dir, 'runs', 'figures', filename)
shutil.copy(filepath, figures_dir)

filename = 'poissonScalingColonialOneAzureA9.png'
filepath = os.path.join(root_dir, 'runs', 'figures', filename)
shutil.copy(filepath, figures_dir)

filename = 'forceCoefficients3d2k35.png'
filepath = os.path.join(root_dir, 'runs', 'batchshipyard', 'snake', '3d',
                        'figures', filename)
shutil.copy(filepath, figures_dir)
