"""
Plots the 3D instantaneous force coefficients obtained on the coarse mesh
(46-million cells) and compare them with previously obtained 2D force
coefficients.
"""

import os
import pathlib
import numpy
from matplotlib import pyplot
pyplot.switch_backend('agg')


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


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent

# Read forces from simulation on coarse mesh
filepath = root_dir / '2k35-meshA/forces.txt'
meshA = read_forces(filepath)

# Read forces from 2D simulation
filepath = root_dir.parent / 'data/forces-2d-2k35.txt'
mesh2d = read_forces(filepath)

# Compute mean force coefficients
spanwise_length = 3.2
get_mean_forces(meshA, time_limits=(50.0, 100.0))
cd3d_mean = 2.0 / spanwise_length * meshA['fx-mean']
cl3d_mean = 2.0 / spanwise_length * meshA['fy-mean']
get_mean_forces(mesh2d, time_limits=(30.0, 80.0))
cd2d_mean = 2.0 * mesh2d['fx-mean']
cl2d_mean = 2.0 * mesh2d['fy-mean']
print('3D <Cd> = {:.4f}'.format(cd3d_mean))
diff = (cd2d_mean - cd3d_mean) / cd3d_mean * 100.0
print('2D <Cd> = {:.4f} ({:.2f}%)'.format(cd2d_mean, diff))
print('3D <Cl> = {:.4f}'.format(cl3d_mean))
diff = (cl2d_mean - cl3d_mean) / cl3d_mean * 100.0
print('2D <Cl> = {:.4f} ({:.2f}%)'.format(cl2d_mean, diff))

# Read force coefficients from Holden et al. (2014)
data_dir = script_dir.parents[4] / 'resources/data'
filepaths = {'cd': data_dir / 'holden_et_al_2014_cd.csv',
             'cl': data_dir / 'holden_et_al_2014_cl.csv'}
holden = {'cd': {}, 'cl': {}}
for key, filepath in filepaths.items():
  with open(filepath, 'r') as infile:
    data = numpy.genfromtxt(filepath,
                            delimiter=',', skip_header=6, usecols=(0, 1, 2))
  for d in data:
    for Re in (3000.0, 5000.0):
      for angle in (30.0, 35.0, 40.0):
        if d[0] == Re and d[1] == angle:
          print('Holden et al. (2014) at Re={}, AoA={}deg: <{}> = {:.4f}'
                .format(Re, angle, key, d[2]))

# Plot forces
pyplot.style.use('seaborn-dark')
fig, ax = pyplot.subplots(2, figsize=(8.0, 4.0), sharex=True)
ax[0].set_ylabel('$C_D$', fontname='DejaVu Serif', fontsize=12)
ax[1].set_ylabel('$C_L$', fontname='DejaVu Serif', fontsize=12)
ax[-1].set_xlabel('non-dimensional time', fontsize=12)
for i, key in enumerate(('fx', 'fy')):
  ax[i].grid()
  ax[i].plot(meshA['times'], 2.0 / spanwise_length * meshA[key],
             label='3D', linestyle='-', linewidth=1.0)
  if i < 2:
    ax[i].plot(mesh2d['times'], 2.0 * mesh2d[key],
               label='2D', linestyle='-', linewidth=1.0)
ax[0].set_xlim(0.0, 100.0)
ax[0].set_ylim(0.5, 1.6)
ax[1].set_ylim(1.0, 3.0)
handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels,
           ncol=2, loc='center', prop={'family': 'serif', 'size': 12},
           frameon=False,
           bbox_to_anchor=(0.55, 0.54))
for a in ax:
  for method in ['get_xticklabels', 'get_yticklabels']:
    for label in getattr(a, method)():
      label.set_fontname('DejaVu Serif')
      label.set_fontsize(12)
fig.tight_layout()

figures_dir = root_dir / 'figures'
figures_dir.mkdir(parents=True, exist_ok=True)
filepath = figures_dir / 'forceCoefficients3d2k35-meshA.png'
fig.savefig(str(filepath), dpi=300, format='png')
