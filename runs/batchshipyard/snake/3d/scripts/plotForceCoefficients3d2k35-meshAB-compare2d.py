"""
Plots the instantaneous force coefficients.
"""

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
    if key != 'times' and 'mean' not in key and value is not None:
      data2[key + '-mean'] = value[mask].mean()
  for key, value in data2.items():
    data[key] = value


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent

# Read forces from simulation on coarse mesh
filepath = root_dir / '2k35-meshA/forces.txt'
meshA = read_forces(filepath)

# Read forces from simulation on fine mesh
filepath = root_dir / '2k35-meshB/forces.txt'
meshB = read_forces(filepath)
# Apply time-correction due to change in time-step size
time_correction = 50.0
meshB['times'] += time_correction
# Re-define time values because of PetIBM 6-digit precision
dt = 5.0E-04
tstart, tend = meshB['times'][0], meshB['times'][-1]
meshB['times'] = numpy.linspace(tstart, tend, meshB['fx'].size)
tstart, tend, dt = meshB['times'][0], meshB['times'][-1], 5.0E-04
assert meshB['times'].size == meshB['fx'].size

# Read forces from simulation on fine mesh (restart)
filepath = root_dir / '2k35-meshB-restart1/forces.txt'
meshB1 = read_forces(filepath)
# Apply time-correction due to change in time-step size
time_correction = 50.0
meshB1['times'] += time_correction
# Re-define time values because of PetIBM 6-digit precision
dt = 5.0E-04
tstart, tend = meshB1['times'][0], meshB1['times'][-1] + dt
meshB1['times'] = numpy.linspace(tstart, tend, meshB1['fx'].size)
assert meshB1['times'].size == meshB1['fx'].size

# Read forces from simulation on fine mesh (second restart)
filepath = root_dir / '2k35-meshB-restart2/forces.txt'
meshB2 = read_forces(filepath)
# Apply time-correction due to change in time-step size
time_correction = 50.0
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
filepath = root_dir.parent / 'data/forces-2d-2k35.txt'
mesh2d = read_forces(filepath)

# Compute mean force coefficients
spanwise_length = 3.2
get_mean_forces(all3d, time_limits=(50.0, 100.0))
cd3dmeshA_mean = 2.0 / spanwise_length * all3d['fx-mean']
cl3dmeshA_mean = 2.0 / spanwise_length * all3d['fy-mean']
get_mean_forces(all3d, time_limits=(100.0, 190.0))
cd3dmeshB_mean = 2.0 / spanwise_length * all3d['fx-mean']
cl3dmeshB_mean = 2.0 / spanwise_length * all3d['fy-mean']
get_mean_forces(mesh2d, time_limits=(30.0, 80.0))
cd2d_mean = 2.0 * mesh2d['fx-mean']
cl2d_mean = 2.0 * mesh2d['fy-mean']
print('3D (meshB) <Cd> = {:.4f}'.format(cd3dmeshB_mean))
diff = (cd3dmeshA_mean - cd3dmeshB_mean) / cd3dmeshB_mean * 100.0
print('3D (meshA) <Cd> = {:.4f} ({:.2f}%)'.format(cd3dmeshA_mean, diff))
diff = (cd2d_mean - cd3dmeshB_mean) / cd3dmeshB_mean * 100.0
print('2D <Cd> = {:.4f} ({:.2f}%)'.format(cd2d_mean, diff))
print('3D (meshB) <Cl> = {:.4f}'.format(cl3dmeshB_mean))
diff = (cl3dmeshA_mean - cl3dmeshB_mean) / cl3dmeshB_mean * 100.0
print('3D (meshA) <Cl> = {:.4f} ({:.2f}%)'.format(cl3dmeshA_mean, diff))
diff = (cl2d_mean - cl3dmeshB_mean) / cl3dmeshB_mean * 100.0
print('2D <Cl> = {:.4f} ({:.2f}%)'.format(cl2d_mean, diff))

# Plot forces
pyplot.style.use('seaborn-dark')
fig, ax = pyplot.subplots(2, figsize=(6.0, 4.0), sharex=True)
ax[0].set_ylabel('$C_D$', fontsize=14)
ax[1].set_ylabel('$C_L$', fontsize=14)
ax[-1].set_xlabel('non-dimensional time', fontsize=12)
for i, key in enumerate(('fx', 'fy')):
  ax[i].grid()
  ax[i].plot(mesh2d['times'], 2.0 * mesh2d[key],
             label='2D (2.9M cells)', color='black', linewidth=0.5)
  ax[i].plot(meshA['times'], 2.0 / spanwise_length * meshA[key],
             label='3D (46M cells)', color='C1', linewidth=1)
  ax[i].plot(meshB['times'], 2.0 / spanwise_length * meshB[key],
             label='3D (233M cells)', color='C0', linewidth=1)
  ax[i].plot(meshB1['times'], 2.0 / spanwise_length * meshB1[key],
             color='C0', linewidth=1)
  ax[i].plot(meshB2['times'], 2.0 / spanwise_length * meshB2[key],
             color='C0', linewidth=1)
ax[0].set_xlim(0.0, 200.0)
ax[0].set_ylim(0.6, 1.5)
ax[1].set_ylim(1.0, 3.0)
handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels,
           ncol=3, loc='center', prop={'family': 'serif', 'size': 10},
           frameon=False,
           bbox_to_anchor=(0.55, 0.54))
fig.tight_layout()

figures_dir = root_dir / 'figures'
figures_dir.mkdir(parents=True, exist_ok=True)
filepath = figures_dir / 'forceCoefficients3d2k35-meshAB-compare2d.png'
fig.savefig(str(filepath), dpi=300, format='png')
