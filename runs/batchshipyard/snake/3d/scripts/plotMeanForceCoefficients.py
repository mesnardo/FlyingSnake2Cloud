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
import numpy
from matplotlib import pyplot
pyplot.switch_backend('agg')


def read_forces(filepath, time_correction=0.0, time_limits=(None, None)):
  with open(filepath, 'r') as infile:
    data = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)
  if all(time_limits):
    # Re-define the time values.
    data[0] = numpy.linspace(*time_limits, data[0].size)
  # Apply time-correction.
  data[0] += time_correction
  return {'t': data[0], 'fx': data[1], 'fy': data[2],
          'fz': (None if len(data) == 3 else data[3])}


def get_mean_forces(data, time_limits=(-numpy.inf, numpy.inf)):
  mask = numpy.where(numpy.logical_and(data['t'] >= time_limits[0],
                                       data['t'] <= time_limits[1]))[0]
  mean = {'t-start': time_limits[0], 't-end': time_limits[1]}
  for key, value in data.items():
    if key in ['fx', 'fy', 'fz']:
      mean[key] = value[mask].mean()
  return mean


def print_mean_forces(mean, label):
  print('{}:'.format(label))
  print('  - time limits: [{:.4f}, {:.4f}]'
        .format(mean['t-start'], mean['t-end']))
  for key, value in mean.items():
    print('  - {}: {:.6f}'.format(key, value))


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent
out_dir = root_dir / 'figures'

# Read forces (1k35, meshA).
filepath = root_dir / '1k35-meshA/forces.txt'
meshA_1k35 = read_forces(filepath, time_limits=(100.0, 200.0))
# Read forces (2k30, meshA).
filepath = root_dir / '2k30-meshA/forces.txt'
meshA_2k30 = read_forces(filepath, time_limits=(100.0, 200.0))
# Read forces (2k35, meshA).
filepath = root_dir / '2k35-meshA/forces.txt'
meshA_2k35 = read_forces(filepath, time_limits=(0.0, 100.0))
# Read forces (2k35, meshB).
filepath = root_dir / '2k35-meshB/forces.txt'
meshB_2k35 = read_forces(filepath, time_limits=(100.0005, 149.3070))
# Read forces (2k35, meshB, first restart).
filepath = root_dir / '2k35-meshB-restart1/forces.txt'
meshB1_2k35 = read_forces(filepath, time_limits=(147.6005, 175.2000))
# Read forces (2k35, meshB, second restart).
filepath = root_dir / '2k35-meshB-restart2/forces.txt'
meshB2_2k35 = read_forces(filepath, time_limits=(174.8005, 190.8000))

# Merge data obtained on meshB for 2k35.
meshB_2k35_all = {}
offset_noise = 800
mask1 = numpy.where(meshB1_2k35['t'] > meshB_2k35['t'][-1])[0]
mask2 = numpy.where(meshB2_2k35['t'] > meshB1_2k35['t'][-1])[0]
for key in meshB_2k35.keys():
  meshB_2k35_all[key] = numpy.concatenate((meshB_2k35[key][offset_noise:],
                                           meshB1_2k35[key][mask1],
                                           meshB2_2k35[key][mask2]))

# Compute mean forces.
meshA_1k35['mean'] = get_mean_forces(meshA_1k35, time_limits=(120.0, 190.0))
print_mean_forces(meshA_1k35['mean'], '1k35-meshA')
meshA_2k30['mean'] = get_mean_forces(meshA_2k30, time_limits=(120.0, 190.0))
print_mean_forces(meshA_2k30['mean'], '2k30-meshA')
meshA_2k35['mean'] = get_mean_forces(meshA_2k35, time_limits=(50.0, 100.0))
print_mean_forces(meshA_2k35['mean'], '2k35-meshA')
meshB_2k35_all['mean'] = get_mean_forces(meshB_2k35_all,
                                         time_limits=(120.0, 190.0))
print_mean_forces(meshB_2k35_all['mean'], '2k35-meshB')

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
Lz = 3.2  # Spanwise length
ax1.scatter(35.0, 2.0 / Lz * meshA_1k35['mean']['fy'],
            label=r'3D ($Re=1000$, $AoA=35^o$)',
            c='C0', s=80, marker='X', edgecolors='black')
ax1.scatter(30.0, 2.0 / Lz * meshA_2k30['mean']['fy'],
            label=r'3D ($Re=2000$, $AoA=30^o$)',
            c='C1', s=80, marker='X', edgecolors='black')
# ax1.scatter(35.0, 2.0 / Lz * meshA_2k35['mean']['fy'],
#             label=r'3D ($Re=2000$, $AoA=35^o$)',
#             c='C2', s=80, marker='X', edgecolors='black')
ax1.scatter(35.0, 2.0 / Lz * meshB_2k35_all['mean']['fy'],
            label=r'3D ($Re=2000$, $AoA=35^o$)',
            c='C2', s=80, marker='X', edgecolors='black')
# Add the time-averaged lift coefficient from previous 2D runs.
ax1.plot(alpha_2d2k, cl_2d2k,
         label=r'2D ($Re=2000$)',
         color='black', marker='x')
ax1.legend(loc='lower right', prop={'size': 12})
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
ax2.scatter(35.0, 2.0 / Lz * meshA_1k35['mean']['fx'],
            label=r'3D ($Re=1000$, $AoA=35^o$)',
            c='C0', s=80, marker='X', edgecolors='black')
ax2.scatter(30.0, 2.0 / Lz * meshA_2k30['mean']['fx'],
            label=r'3D ($Re=2000$, $AoA=30^o$)',
            c='C1', s=80, marker='X', edgecolors='black')
# ax2.scatter(35.0, 2.0 / Lz * meshA_2k35['mean']['fx'],
#             label=r'3D ($Re=2000$, $AoA=35^o$)',
#             c='C2', s=80, marker='X', edgecolors='black')
ax2.scatter(35.0, 2.0 / Lz * meshB_2k35_all['mean']['fx'],
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
