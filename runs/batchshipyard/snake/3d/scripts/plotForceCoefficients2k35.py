"""
Plots the instantaneous force coefficients.
"""

import os
import numpy
from matplotlib import pyplot
pyplot.switch_backend('agg')


if not os.environ.get('AZ_SNAKE'):
  raise KeyError('Environment variable AZ_SNAKE is not set')


def read_forces(filepath):
  with open(filepath, 'r') as infile:
    data = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)
  return {'times': data[0],
          'fx': data[1], 'fy': data[2],
          'fz': (None if len(data) == 3 else data[3])}


def get_mean_forces(data, time_limits=(-numpy.inf, numpy.inf)):
  mask = numpy.where(numpy.logical_and(data['times'] >= time_limits[0],
                                       data['times'] <= time_limits[1]))[0]
  data2 = {}
  for key, value in data.items():
    if key != 'times' and value is not None:
      data2[key + '-mean'] = value[mask].mean()
  for key, value in data2.items():
    data[key] = value


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.sep.join(script_dir.split(os.sep)[:-1])

spanwise_length = 3.2
time_correction = 50.0

# Read forces from simulation on coarse mesh
filepath = os.path.join(root_dir, '2k35-meshA', 'forces.txt')
meshA = read_forces(filepath)

# Read forces from simulation on fine mesh
filepath = os.path.join(root_dir, '2k35-meshB', 'forces.txt')
meshB = read_forces(filepath)
# Apply time-correction due to change in time-step size
meshB['times'] += time_correction
# Re-define time values because of PetIBM 6-digit precision
dt = 5.0E-04
tstart, tend = meshB['times'][0], meshB['times'][-1]
meshB['times'] = numpy.linspace(tstart, tend, meshB['fx'].size)
tstart, tend, dt = meshB['times'][0], meshB['times'][-1], 5.0E-04
assert meshB['times'].size == meshB['fx'].size

# Read forces from simulation on fine mesh (restart)
filepath = os.path.join(root_dir, '2k35-meshB-restart1', 'forces.txt')
meshB1 = read_forces(filepath)
# Apply time-correction due to change in time-step size
meshB1['times'] += time_correction
# Re-define time values because of PetIBM 6-digit precision
dt = 5.0E-04
tstart, tend = meshB1['times'][0], meshB1['times'][-1] + dt
meshB1['times'] = numpy.linspace(tstart, tend, meshB1['fx'].size)
assert meshB1['times'].size == meshB1['fx'].size

# Read forces from simulation on fine mesh (second restart)
filepath = os.path.join(root_dir, '2k35-meshB-restart2', 'forces.txt')
meshB2 = read_forces(filepath)
# Apply time-correction due to change in time-step size
meshB2['times'] += time_correction
# Re-define time values because of PetIBM 6-digit precision
dt = 5.0E-04
tstart, tend = meshB2['times'][0] + dt, meshB2['times'][-1] + dt
meshB2['times'] = numpy.linspace(tstart, tend, meshB2['fx'].size)
assert meshB2['times'].size == meshB2['fx'].size

# Concatenate results from all 3D runs
all3d = {}
offset_noise = 800
mask1 = numpy.where(meshB1['times'] > meshB['times'][-1])[0]
mask2 = numpy.where(meshB2['times'] > meshB1['times'][-1])[0]
for key in meshA.keys():
  all3d[key] = numpy.concatenate((meshA[key],
                                  meshB[key][offset_noise:],
                                  meshB1[key][mask1],
                                  meshB2[key][mask2]))

# Read forces from 2D simulation
filepath = os.path.join(os.environ['AZ_SNAKE'], 'runs', 'batchshipyard',
                        'snake', 'data', 'forces-2d-2k35.txt')
mesh2d = read_forces(filepath)

# Compute mean force coefficients
get_mean_forces(all3d, time_limits=(50.0, 150.0))
cd3d_mean = 2.0 / spanwise_length * all3d['fx-mean']
cl3d_mean = 2.0 / spanwise_length * all3d['fy-mean']
get_mean_forces(mesh2d, time_limits=(32.0, 64.0))
cd2d_mean = 2.0 * mesh2d['fx-mean']
cl2d_mean = 2.0 * mesh2d['fy-mean']
print('3D <Cd> = {:.4f}'.format(cd3d_mean))
diff = (cd2d_mean - cd3d_mean) / cd3d_mean * 100.0
print('2D <Cd> = {:.4f} ({:.2f}%)'.format(cd2d_mean, diff))
print('3D <Cl> = {:.4f}'.format(cl3d_mean))
diff = (cl2d_mean - cl3d_mean) / cl3d_mean * 100.0
print('2D <Cl> = {:.4f} ({:.2f}%)'.format(cl2d_mean, diff))

# Plot forces
pyplot.style.use('seaborn-dark')
fig, ax = pyplot.subplots(2, figsize=(6.0, 6.0), sharex=True)
ax[0].set_ylabel('$C_D$', fontsize=16)
ax[1].set_ylabel('$C_L$', fontsize=16)
ax[-1].set_xlabel('non-dimensional time', fontsize=16)
for i, key in enumerate(('fx', 'fy')):
  ax[i].grid()
  ax[i].plot(meshA['times'], 2.0 / spanwise_length * meshA[key],
             label='mesh A', linewidth=1)
  ax[i].plot(meshB['times'], 2.0 / spanwise_length * meshB[key],
             label='mesh B', linewidth=1)
  ax[i].plot(meshB1['times'], 2.0 / spanwise_length * meshB1[key],
             label='mesh B (first restart)', linewidth=1)
  ax[i].plot(meshB2['times'], 2.0 / spanwise_length * meshB2[key],
             label='mesh B (second restart)', linewidth=1)
  ax[i].plot(all3d['times'], 2.0 / spanwise_length * all3d[key],
             label='all 3D runs', linestyle='--', linewidth=1)
  if i < 2:
    ax[i].plot(mesh2d['times'], 2.0 * mesh2d[key],
               label='2D mesh', linewidth=1)
ax[0].set_xlim(0.0, 200.0)
ax[0].set_ylim(0.5, 1.6)
ax[1].set_ylim(1.0, 3.0)
handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels,
           ncol=3, loc='center', prop={'family': 'serif', 'size': 10},
           frameon=False,
           bbox_to_anchor=(0.55, 0.525))
fig.tight_layout()

figures_dir = os.path.join(root_dir, 'figures')
if not os.path.isdir(figures_dir):
  os.makedirs(figures_dir)
filepath = os.path.join(figures_dir, 'forceCoefficients2k35.png')
fig.savefig(filepath, dpi=300, format='png')
