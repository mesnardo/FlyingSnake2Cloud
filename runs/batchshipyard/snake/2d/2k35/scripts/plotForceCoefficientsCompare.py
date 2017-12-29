"""
Post-processes the force coefficients from a PetIBM simulation.

This script reads the forces, computes the mean forces within a given range,
computes the Strouhal number within a range, plots the force coefficients,
saves the figure, and prints a data-frame that contains the mean values.
"""

import os
from matplotlib import pyplot
from snake.petibm.simulation import PetIBMSimulation


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

# Time limits used to average the quantities.
time_limits = (32.0, 64.0)

dataframes = []

directory = root_dir
simu1 = PetIBMSimulation(description='Batch Shipyard', directory=directory)
simu1.read_forces()
# simu1.get_mean_forces(limits=time_limits)
# simu1.get_strouhal(limits=time_limits, order=200)
# dataframes.append(simu1.create_dataframe_forces(display_strouhal=True,
#                                                 display_coefficients=True,
#                                                 coefficient=2.0))

directory = os.path.join(os.environ['HOME'], 'git', 'mesnardo', 'snakeLips',
                         'simulations', 'Re2000', 'both', 'aoa35')
simu2 = PetIBMSimulation(description='Colonialone', directory=directory)
simu2.read_forces()
# simu2.get_mean_forces(limits=time_limits)
# simu2.get_strouhal(limits=time_limits, order=200)
# dataframes.append(simu2.create_dataframe_forces(display_strouhal=True,
#                                                 display_coefficients=True,
#                                                 coefficient=2.0))

# Print time-averaged quantities for all runs considered.
# print(dataframes[0].append(dataframes[1:]))

# Plot instantaneous force coefficients vs. time units.
pyplot.style.use('seaborn-dark')
fig, ax = pyplot.subplots(2, figsize=(10.0, 6.0), sharex=True)
ax[0].grid(zorder=0)
ax[0].set_ylabel('$C_D$', fontname='DejaVu Serif', fontsize=16)
ax[0].plot(simu1.forces[0].times, 2.0 * simu1.forces[0].values,
           label=simu1.description, linewidth=1, linestyle='-', zorder=10)
ax[0].plot(simu2.forces[0].times, 2.0 * simu2.forces[0].values,
           label=simu2.description, linewidth=1, linestyle='--', zorder=10)
ax[0].set_ylim(0.5, 3.5)
ax[1].grid(zorder=0)
ax[1].set_xlabel('non-dimensional time unit',
                 fontname='DejaVu Serif', fontsize=16)
ax[1].set_ylabel('$C_L$', fontname='DejaVu Serif', fontsize=16)
ax[1].plot(simu1.forces[1].times, 2.0 * simu1.forces[1].values,
           label=simu1.description, linewidth=1, linestyle='-', zorder=10)
ax[1].plot(simu2.forces[1].times, 2.0 * simu2.forces[1].values,
           label=simu2.description, linewidth=1, linestyle='--', zorder=10)
ax[1].set_xlim(0.0, 80.0)
ax[1].set_ylim(0.0, 3.0)
for a in ax:
  for method in ['get_xticklabels', 'get_yticklabels']:
    for label in getattr(a, method)():
      label.set_fontname('DejaVu Serif')
      label.set_fontsize(14)
handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels,
           ncol=2, loc='center', prop={'family': 'serif', 'size': 16},
           frameon=False,
           bbox_to_anchor=(0.50, 0.52))
fig.tight_layout()

pyplot.show()
