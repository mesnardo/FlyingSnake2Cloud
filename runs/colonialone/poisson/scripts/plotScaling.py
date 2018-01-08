"""
Plot strong scaling.
"""

import os
import numpy
from matplotlib import pyplot


def get_runtime(filepath, offset=7):
  with open(filepath, 'r') as infile:
    runtime = float(infile.readlines()[-offset:][0].split()[-1])
  return runtime


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.sep.join(script_dir.split(os.sep)[:-1])

max_nodes = 8
nodes = numpy.arange(1, max_nodes + 1)

folders = ['run1', 'run2', 'run3', 'run4', 'run5']

runtimes = numpy.empty((len(folders), max_nodes), dtype=numpy.float64)
for i, folder in enumerate(folders):
  for j, node in enumerate(nodes):
    filename = ('poisson-hypre-{}node'.format(node) +
                ('s' if node != 1 else '') +
                '.out')
    filepath = os.path.join(root_dir, folder, filename)
    runtimes[i, j] = get_runtime(filepath)

mean_runtimes = runtimes.mean(axis=0)
min_runtimes = runtimes.min(axis=0)
max_runtimes = runtimes.max(axis=0)

pyplot.style.use('seaborn-dark')
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_title('Poisson system (46M unknowns)', fontsize=16)
ax.yaxis.grid(zorder=0)
ax.set_xlabel('Number of CPU nodes', fontsize=16)
ax.set_ylabel('Time (seconds)', fontsize=16)
bar_width = 0.25
offset = 0.125
ax.bar(nodes + offset, mean_runtimes, bar_width,
       label='Colonial One', linewidth=0)
ax.errorbar(nodes + offset, mean_runtimes,
            [mean_runtimes - min_runtimes, max_runtimes - mean_runtimes],
            fmt='.k', ecolor='black', elinewidth=2,
            capthick=2, capsize=4, barsabove=True)
ax.legend(loc='upper right', prop={'size': 16}, frameon=False)
ax.tick_params(axis='both', labelsize=16)
fig.tight_layout()

figures_dir = os.path.join(root_dir, 'figures')
if not os.path.isdir(figures_dir):
  os.makedirs(figures_dir)
filepath = os.path.join(figures_dir, 'poissonScalingColonialOne.png')
fig.savefig(filepath)

pyplot.show()
