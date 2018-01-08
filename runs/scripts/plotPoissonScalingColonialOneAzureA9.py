"""
Plot strong scaling.
"""

import os
import numpy
from matplotlib import pyplot
pyplot.switch_backend('agg')


def get_runtime(filepath, offset=7):
  with open(filepath, 'r') as infile:
    runtime = float(infile.readlines()[-offset:][0].split()[-1])
  return runtime


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.sep.join(script_dir.split(os.sep)[:-1])

cases = {}

max_nodes = 8
nodes = numpy.arange(1, max_nodes + 1)

# Read runtimes from Colonial One runs
common_dir = os.path.join(root_dir, 'colonialone', 'poisson')
folders = ['run1', 'run2', 'run3', 'run4', 'run5']
folders = ['run1']
cases['Colonial One'] = {}
runtimes = numpy.empty((len(folders), max_nodes), dtype=numpy.float64)
for i, folder in enumerate(folders):
  for j, node in enumerate(nodes):
    filename = ('poisson-hypre-{}node'.format(node) +
                ('s' if node != 1 else '') +
                '.out')
    filepath = os.path.join(common_dir, folder, filename)
    runtimes[i, j] = get_runtime(filepath)

cases['Colonial One']['runtimes'] = runtimes
cases['Colonial One']['mean'] = runtimes.mean(axis=0)
cases['Colonial One']['min'] = runtimes.min(axis=0)
cases['Colonial One']['max'] = runtimes.max(axis=0)

# Read runtimes from Azure A9 runs
common_dir = os.path.join(root_dir, 'azure-A9cluster',
                          'poisson', 'uniform2')
folders = ['run1', 'run2', 'run3', 'run4', 'run5']
cases['Azure A9'] = {}
runtimes = numpy.empty((len(folders), max_nodes), dtype=numpy.float64)
for i, folder in enumerate(folders):
  for j, node in enumerate(nodes):
    filename = ('output-{}node'.format(node) +
                ('s' if node != 1 else '') +
                '.txt')
    filepath = os.path.join(common_dir, folder, filename)
    runtimes[i, j] = get_runtime(filepath)

cases['Azure A9']['runtimes'] = runtimes
cases['Azure A9']['mean'] = runtimes.mean(axis=0)
cases['Azure A9']['min'] = runtimes.min(axis=0)
cases['Azure A9']['max'] = runtimes.max(axis=0)

# Plot scaling results
pyplot.style.use('seaborn-dark')
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.yaxis.grid(zorder=0)
ax.set_xlabel('Number of CPU nodes', fontsize=16)
ax.set_ylabel('Time (seconds)', fontsize=16)
bar_width = 0.25
offset = 0.125
ax.bar(nodes + offset, cases['Colonial One']['mean'], bar_width,
       label='Colonial One', linewidth=0)
ax.errorbar(nodes + offset, cases['Colonial One']['mean'],
            [cases['Colonial One']['mean'] - cases['Colonial One']['min'],
             cases['Colonial One']['max'] - cases['Colonial One']['mean']],
            fmt='.k', ecolor='black', elinewidth=2,
            capthick=2, capsize=4, barsabove=True)
offset = -0.125
ax.bar(nodes + offset, cases['Azure A9']['mean'], bar_width,
       label='Azure A9', linewidth=0)
ax.errorbar(nodes + offset, cases['Azure A9']['mean'],
            [cases['Azure A9']['mean'] - cases['Azure A9']['min'],
             cases['Azure A9']['max'] - cases['Azure A9']['mean']],
            fmt='.k', ecolor='black', elinewidth=2,
            capthick=2, capsize=4, barsabove=True)
ax.legend(loc='upper right', prop={'size': 16}, frameon=False)
ax.tick_params(axis='both', labelsize=16)
fig.tight_layout()

figures_dir = os.path.join(root_dir, 'figures')
if not os.path.isdir(figures_dir):
    os.makedirs(figures_dir)
save_path = os.path.join(figures_dir, 'poissonScalingColonialOneAzureA9.png')
fig.savefig(save_path, dpi=300)
