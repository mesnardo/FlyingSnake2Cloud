"""
Plots the force coefficients.
"""

import os
import collections
import itertools
import numpy
from matplotlib import pyplot


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

runs = collections.OrderedDict()

directory = os.path.join(root_dir, 'ibpm', 'amgx_aggregation')
filepath = os.path. join(directory, 'forces.txt')
with open(filepath, 'r') as infile:
  runs['IBPM (AmgX aggregation)'] = numpy.loadtxt(infile,
                                                  dtype=numpy.float64,
                                                  unpack=True)

directory = os.path.join(root_dir, 'decoupled', 'amgx_classical')
filepath = os.path. join(directory, 'forces.txt')
with open(filepath, 'r') as infile:
  runs['decoupled (AmgX classical)'] = numpy.loadtxt(infile,
                                                     dtype=numpy.float64,
                                                     unpack=True)

coeff = 2.0

pyplot.style.use('seaborn-dark')

fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.grid()
ax.set_xlabel('time unit', fontsize=16)
ax.set_ylabel('force coefficients', fontsize=16)
linestyles = itertools.cycle(['--', '-', ':'])
zorder = 14
for label, run in runs.items():
  color = next(ax._get_lines.prop_cycler)['color']
  linestyle = next(linestyles)
  ax.plot(run[0], coeff * run[1], label=label,
          color=color, linestyle=linestyle, zorder=zorder)
  ax.plot(run[0], coeff * run[2],
          color=color, linestyle=linestyle, zorder=zorder)
  zorder -= 1
ax.legend(loc='lower center', prop={'size': 14}, ncol=2, frameon=True)
ax.set_xlim(0.0, 80.0)
ax.set_ylim(0.0, 2.5)
ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)
fig.tight_layout()

figures_dir = os.path.join(root_dir, 'figures')
if not os.path.isdir(figures_dir):
    os.makedirs(figures_dir)
save_path = os.path.join(figures_dir, 'forceCoefficients2k30.png')
fig.savefig(save_path, dpi=300)

pyplot.show()
