"""
Plots the time-averaged force coefficients obtained with 3D simulations.
Compares with force coefficients from Holden et al. (2014).
Compares with time-averaged force coefficients obtained with previous 2D
simulations run with PetIBM.

References:
- Holden, D., Socha, J. J., Cardwell, N. D., & Vlachos, P. P. (2014).
  Aerodynamics of the flying snake Chrysopelea paradisi: how a bluff body
  cross-sectional shape contributes to gliding performance.
  Journal of Experimental Biology, 217(3), 382-394.
"""

import pathlib
import yaml
from matplotlib import pyplot
pyplot.switch_backend('agg')


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent
out_dir = root_dir / 'figures'

# Get the time-averaged force coefficients from 3D PetIBM runs.
data3d = {}
data3d['1k35'] = {'Re': 1000.0, 'alpha': 35.0, 'cd': 0.8503, 'cl': 1.5393}
data3d['2k30'] = {'Re': 2000.0, 'alpha': 30.0, 'cd': 0.7379, 'cl': 1.4895}
data3d['2k35'] = {'Re': 2000.0, 'alpha': 35.0, 'cd': 0.7882, 'cl': 1.5236}

# Get the time-averaged force coefficients from previous 2D PetIBM runs.
# The instantaneous force coefficient were averaged
# between 32 and 64 time-units of flow simulation.
data_dir = root_dir.parent / 'data'
filepath = data_dir / 'forceCoefficientsVsAoA2d2k.yaml'
with open(filepath, 'r') as infile:
  data2d = yaml.load(infile)
alpha_2d2k = data2d['angles']
cd_2d2k = data2d['cd']['both']
cl_2d2k = data2d['cl']['both']

# Plots the time-averaged force coefficients versus the angle of attack.
fig, (ax1, ax2) = pyplot.subplots(nrows=1, ncols=2, figsize=(10.0, 6.0))
# Lift coefficient.
ax1.grid(False)
ax1.set_xlabel('Angle of attack (deg)', fontsize=14)
ax1.set_ylabel(r'$C_L$', fontsize=16)
# Add the time-averaged lift coefficient from present 3D runs.
ax1.scatter(data3d['1k35']['alpha'], data3d['1k35']['cl'],
            label=r'3D ($Re=1000$, $AoA=35^o$)',
            c='C0', s=80, marker='X', edgecolors='black')
ax1.scatter(data3d['2k30']['alpha'], data3d['2k30']['cl'],
            label=r'3D ($Re=2000$, $AoA=30^o$)',
            c='C1', s=80, marker='X', edgecolors='black')
ax1.scatter(data3d['2k35']['alpha'], data3d['2k35']['cl'],
            label=r'3D ($Re=2000$, $AoA=35^o$)',
            c='C2', s=80, marker='X', edgecolors='black')
# Add the time-averaged lift coefficient from previous 2D runs.
ax1.plot(alpha_2d2k, cl_2d2k,
         label=r'2D ($Re=2000$)',
         color='black', marker='x')
ax1.legend(loc='lower right', prop={'size': 10})
xmin, xmax = -10.0, 60.0
ymin, ymax = -1.0, 2.0
ax1.set_xlim(xmin, xmax)
ax1.set_ylim(ymin, ymax)
# Add the lift coefficients from Holden et al. (2014) as a background image
# of the present figure.
filepath = data_dir / 'holden_et_al_2014_cl.png'
img = pyplot.imread(str(filepath))
aspect = (xmax - xmin) / (ymax - ymin)
ax1.imshow(img, extent=[xmin, xmax, ymin, ymax], aspect=aspect)
# Drag coefficient.
ax2.grid(False)
ax2.set_xlabel('Angle of attack (deg)', fontsize=14)
ax2.set_ylabel(r'$C_D$', fontsize=16)
# Add the time-averaged drag coefficient from present 3D runs.
ax2.scatter(data3d['1k35']['alpha'], data3d['1k35']['cd'],
            label=r'3D ($Re=1000$, $AoA=35^o$)',
            c='C0', s=80, marker='X', edgecolors='black')
ax2.scatter(data3d['2k30']['alpha'], data3d['2k30']['cd'],
            label=r'3D ($Re=2000$, $AoA=30^o$)',
            c='C1', s=80, marker='X', edgecolors='black')
ax2.scatter(data3d['2k35']['alpha'], data3d['2k35']['cd'],
            label=r'3D ($Re=2000$, $AoA=35^o$)',
            c='C2', s=80, marker='X', edgecolors='black')
# Add the time-averaged drag coefficient from previous 2D runs.
ax2.plot(alpha_2d2k, cd_2d2k,
         label=r'2D ($Re=2000$)',
         color='black', marker='x')
xmin, xmax = -10.0, 60.0
ymin, ymax = 0.0, 2.0
ax2.set_xlim(xmin, xmax)
ax2.set_ylim(ymin, ymax)
# Add the drag coefficients from Holden et al. (2014) as a background image
# of the present figure.
filepath = data_dir / 'holden_et_al_2014_cd.png'
img = pyplot.imread(str(filepath))
aspect = (xmax - xmin) / (ymax - ymin)
ax2.imshow(img, extent=[xmin, xmax, ymin, ymax], aspect=aspect)
fig.tight_layout()
# Save the figure as a png file.
filepath = out_dir / 'meanForceCoefficients.png'
out_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(str(filepath), dpi=300, format='png')
