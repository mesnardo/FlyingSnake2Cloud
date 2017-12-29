"""
Plots bar charts with the wall-time (in seconds and percent of the total
wall-time) of all PETSc events registered for a PetIBM run.
"""

import os
import itertools
from matplotlib import pyplot
from snake.petibm import logViewReader


filepath = os.path.join(os.getcwd(), 'log2442548.out')
run1 = logViewReader.Run(label='classical', logpath=filepath)
run1.get_walltime()
run1.get_events()
run1.get_resident_set_size(unit='GB')
print('RES = {:6f} GB'.format(run1.res))

filepath = os.path.join(os.pardir, 'meshA', 'log2442507.out')
run2 = logViewReader.Run(label='aggregation', logpath=filepath)
run2.get_walltime()
run2.get_events()
run2.get_resident_set_size(unit='GB')
print('RES = {:6f} GB'.format(run2.res))

pyplot.style.use('seaborn-dark')
colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c',
          '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00',
          '#cab2d6', '#6a3d9a']
event_labels = list(run1.events.keys())
logViewReader.plot_breakdown_walltimes([run1, run2],
                                       event_labels=event_labels,
                                       colors=itertools.cycle(colors))

logViewReader.plot_breakdown_percents([run1, run2],
                                      event_labels=event_labels,
                                      colors=itertools.cycle(colors))

pyplot.show()
