"""
Plots the instantaneous force coefficients obtained on meshA at Reynolds number
2000 and angle of attack 30 degrees.
Compares the 3D force coefficients with the 2D force coefficients from a
previous simulations.
"""

import os
import pathlib
import numpy
from matplotlib import pyplot
pyplot.switch_backend('agg')


if not os.environ.get('AZ_SNAKE'):
  raise KeyError('Environment variable AZ_SNAKE is not set')


def read_forces(filepath):
  """
  Reads the time values and the force coefficients from a given file.

  Parameters
  ----------
  filepath: str or pathlib.Path
    Path of the file to read.

  Returns
  -------
  dict: dict of (str, numpy.ndarray)
    A dictionary with keys: 'times', 'fx', 'fy', and 'fz'.
    dict['fz'] is set to None for 2D coefficients.
  """
  with open(filepath, 'r') as infile:
    data = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)
  return {'times': data[0],
          'fx': data[1],
          'fy': data[2],
          'fz': (None if len(data) == 3 else data[3])}


def get_mean_forces(data, time_limits=(-numpy.inf, numpy.inf)):
  mask = numpy.where((data['times'] >= time_limits[0]) &
                     (data['times'] <= time_limits[1]))
  keys = ['fx', 'fy']
  if data['fz'] is not None:
    keys.append('fz')
  return (data[k][mask].mean() for k in keys)


def get_mean_force_coefficients(data,
                                time_limits=(-numpy.inf, numpy.inf),
                                coeff=1.0):
  return (coeff * v for v in get_mean_forces(data, time_limits=time_limits))


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent

# Read forces from simulation on coarse mesh.
filepath = root_dir / '2k30-meshA/forces.txt'
meshA = read_forces(filepath)

# Read forces from 2D simulation.
filepath = root_dir.parent / 'data/forces-2d-2k30.txt'
mesh2d = read_forces(filepath)

# Compute 3D mean force coefficients averaged between 150 and 200 time units.
spanwise_length = 3.2
cd, cl, _ = get_mean_force_coefficients(meshA,
                                        time_limits=(150.0, 200.0),
                                        coeff=2.0 / spanwise_length)

# Compute 2D mean force coefficients averaged between 30 and 80 time units.
cd_2d, cl_2d = get_mean_force_coefficients(mesh2d,
                                           time_limits=(30.0, 80.0),
                                           coeff=2.0)

# Prints the mean force coefficients with the relative differences.
print('- 3D:')
print('  + Cd = {:.4f}'.format(cd))
print('  + Cl = {:.4f}'.format(cl))
print('- 2D:')
print('  + Cd = {:.4f} ({:.2f}%)'.format(cd_2d, (cd_2d - cd) / cd * 100))
print('  + Cl = {:.4f} ({:.2f}%)'.format(cl_2d, (cl_2d - cl) / cl * 100))

# Plot the instantaneous force coefficients.
pyplot.style.use('seaborn-dark')
width, height = 10.0, 6.0
gridspec_kw = {'width_ratios': [80 / 280 * width, 100 / 280 * width]}
fig, ((ax1, ax2), (ax3, ax4)) = pyplot.subplots(2, 2,
                                                figsize=(width, height),
                                                gridspec_kw=gridspec_kw,
                                                sharex='col', sharey='row')
# Add 2D drag coefficient.
ax1.set_title('2D mesh (2.9M cells)', fontname='DejaVu Serif', fontsize=14)
ax1.grid()
ax1.set_ylabel('$C_D$', fontname='DejaVu Serif', fontsize=14)
ax1.set_xlim(0.0, 80.0)
ax1.set_ylim(0.6, 1.5)
ax1.set_xticks(numpy.arange(0.0, 80.0 + 1, 20.0))
ax1.plot(mesh2d['times'], 2.0 * mesh2d['fx'],
         label='2D mesh (2.9M cells)', color='grey', linewidth=1.0)
# Add 2D lift coefficient.
ax3.grid()
ax3.set_xlabel('non-dimensional time', fontname='DejaVu Serif', fontsize=12)
ax3.set_ylabel('$C_L$', fontname='DejaVu Serif', fontsize=14)
ax3.set_ylim(1.0, 2.8)
ax3.plot(mesh2d['times'], 2.0 * mesh2d['fy'],
         label='2D mesh (2.9M cells)', color='grey', linewidth=1.0)
# Add 3D drag coefficient.
ax2.set_title('3D mesh (46M cells)', fontname='DejaVu Serif', fontsize=14)
ax2.grid()
ax2.set_xlim(100.0, 200.0)
ax2.set_xticks(numpy.arange(100.0, 200.0 + 1, 20.0))
ax2.plot(meshA['times'], 2.0 / spanwise_length * meshA['fx'],
         label='3D mesh (46M cells)', color='grey', linewidth=1.0)
# Add 2D lift coefficient.
ax4.grid()
ax4.set_xlabel('non-dimensional time', fontname='DejaVu Serif', fontsize=12)
ax4.plot(meshA['times'], 2.0 / spanwise_length * meshA['fy'],
         label='3D mesh (46M cells)', color='grey', linewidth=1.0)
# Set font for axis labels.
for ax in (ax1, ax2, ax3, ax4):
  for method in ['get_xticklabels', 'get_yticklabels']:
    for label in getattr(ax, method)():
      label.set_fontname('DejaVu Serif')
      label.set_fontsize(12)
fig.tight_layout()

figures_dir = root_dir / 'figures'
figures_dir.mkdir(parents=True, exist_ok=True)
filepath = figures_dir / 'forceCoefficients3d2k30-meshA.png'
fig.savefig(str(filepath), dpi=300, format='png')
