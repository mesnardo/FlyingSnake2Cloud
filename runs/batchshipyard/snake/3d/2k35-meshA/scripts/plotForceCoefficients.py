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
data_dir = os.sep.join(script_dir.split(os.sep)[:-1])

# Read forces from 3D simulation
filepath = os.path.join(data_dir, 'forces.txt')
meshA = read_forces(filepath)

# Read forces from 2D simulation
filepath = os.path.join(os.environ['AZ_SNAKE'], 'runs', 'batchshipyard',
                        'snake', 'data', 'forces-2d-2k35.txt')
mesh2d = read_forces(filepath)

# Compute mean force coefficients
spanwise_length = 3.2
get_mean_forces(meshA, time_limits=(50.0, 100.0))
cd3d_mean = 2.0 / spanwise_length * meshA['fx-mean']
cl3d_mean = 2.0 / spanwise_length * meshA['fy-mean']
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
             label='mesh A')
  if i < 2:
    ax[i].plot(mesh2d['times'], 2.0 * mesh2d[key], label='2D mesh')
ax[0].set_ylim(-0.5, 2.5)
ax[1].set_ylim(0.0, 4.5)
handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels,
           ncol=3, loc='center', prop={'family': 'serif', 'size': 12},
           frameon=False,
           bbox_to_anchor=(0.55, 0.525))
fig.tight_layout()

figures_dir = os.path.join(data_dir, 'figures')
if not os.path.isdir(figures_dir):
  os.makedirs(figures_dir)
filepath = os.path.join(figures_dir, 'forceCoefficients.png')
fig.savefig(filepath, dpi=300, format='png')
