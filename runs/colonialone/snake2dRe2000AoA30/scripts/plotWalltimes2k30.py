"""
Plots bar charts with the wall-time (in seconds and percent of the total
wall-time) of all PETSc events registered for a PetIBM run.
"""

import os
import collections
import numpy
from matplotlib import pyplot
from snake.petibm import logViewReader


def get_data(label, filepath):
  run = logViewReader.Run(label=label, logpath=filepath)
  run.get_walltime()
  run.get_events()
  run.get_resident_set_size(unit='GB')
  print(label)
  print('\twalltime: {} s'.format(run.walltime))
  print('\tRES: {} GB'.format(run.res))
  return run


def plot_walltimes(ax, runs, event_labels):
  pyplot.gca().set_prop_cycle(None)
  indices = numpy.arange(len(runs))
  bar_width = 0.5
  bar_offsets = numpy.zeros(len(runs))
  for label, event_name in event_labels.items():
    color = next(ax._get_lines.prop_cycler)['color']
    walltimes = []
    for run in runs:
      if event_name in run.events.keys():
        walltimes.append(run.events[event_name]['walltime'] / 3600.0)
      else:
        walltimes.append(0.0)
    ax.bar(indices, walltimes, bar_width,
           label=label,
           bottom=bar_offsets,
           color=color,
           linewidth=0,
           zorder=0)
    bar_offsets += walltimes
  tick_offset = 0.0
  ax.set_xticks(indices + tick_offset * bar_width)
  ax.set_xticklabels([run.label for run in runs], rotation=45.0, fontsize=14)
  ax.set_xlim(indices[0] - 0.5, indices[-1] + 1.0)


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

runs = []

label = 'IBPM\n(PETSc GAMG)'
directory = os.path.join(root_dir, 'ibpm', 'ksp_gamg')
filepath = os.path.join(directory, 'log1845095.out')
runs.append(get_data(label, filepath))


label = 'IBPM\n(AgmX aggregation)'
directory = os.path.join(root_dir, 'ibpm', 'amgx_aggregation')
filepath = os.path.join(directory, 'log2552123.out')
runs.append(get_data(label, filepath))

label = 'decoupled\n(Hypre BoomerAMG)'
directory = os.path.join(root_dir, 'decoupled', 'ksp_hypre')
filepath = os.path.join(directory, 'log2553064.out')
runs.append(get_data(label, filepath))

label = 'decoupled\n(AmgX classical)'
directory = os.path.join(root_dir, 'decoupled', 'amgx_classical')
filepath = os.path.join(directory, 'log2549518.out')
runs.append(get_data(label, filepath))


event_labels = collections.OrderedDict()
event_labels['Poisson solver'] = 'solvePoisson'
event_labels['Velocity solver'] = 'solveVelocity'
event_labels['setup velocity RHS'] = 'RHSVelocity'
event_labels['Forces solver'] = 'solveForces'
event_labels['setup Poisson RHS'] = 'RHSPoisson'
event_labels['initialization'] = 'initialize'
event_labels['projection step'] = 'projectionStep'


pyplot.style.use('seaborn-dark')

fig, ax = pyplot.subplots(figsize=(10.0, 4.0))
ax.yaxis.grid(zorder=0)
ax.set_ylabel('wall-time (hours)', fontsize=16)
indices = numpy.arange(len(runs))
bar_width = 0.25
bar_offsets = numpy.zeros(len(runs))
for key, value in event_labels.items():
  color = next(ax._get_lines.prop_cycler)['color']
  walltimes = []
  for run in runs:
    if value in run.events.keys():
      walltimes.append(run.events[value]['walltime'] / 3600.0)
    else:
      walltimes.append(0.0)
  ax.bar(indices, walltimes, bar_width,
         label=key,
         bottom=bar_offsets,
         color=color,
         linewidth=0,
         zorder=0)
  bar_offsets += walltimes
for i, run in enumerate(runs[1:]):
  ax.text(indices[i + 1] - bar_width / 2, bar_offsets[i + 1] + 5.0,
          'x{:.1f}'.format(runs[0].walltime / run.walltime),
          fontsize=20)
ax.legend(bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=14)
tick_offset = 0.0
ax.set_xticks(indices + tick_offset * bar_width)
ax.set_xticklabels([run.label for run in runs], rotation=0.0, fontsize=16)
ax.set_xlim(indices[0] - 0.5, indices[-1] + 1.0)
fig.tight_layout()

figures_dir = os.path.join(root_dir, 'figures')
if not os.path.isdir(figures_dir):
    os.makedirs(figures_dir)
save_path = os.path.join(figures_dir, 'walltimes2k30.png')
fig.savefig(save_path, dpi=300)

pyplot.show()
