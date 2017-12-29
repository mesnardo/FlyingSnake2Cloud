"""
Plots the latency and the bandwidth results from the OSU benchmark obtained on
Colonial One and Azure.
"""

import os
import re
import numpy
from matplotlib import pyplot


def get_data(case, filepath, key=None, keys=[], skiplines=0):
  sizes, data = [], []
  with open(filepath, 'r') as infile:
    lines = infile.readlines()[skiplines:]
    for line in lines:
      if re.match(r"^\d+.*$", line):
        size, dat = line.strip().split()
        sizes.append(int(size))
        data.append(float(dat))
  if key:
    case[key] = {'sizes': sizes, 'data': data}
  elif len(keys) > 0:
    indices = numpy.append(numpy.where(numpy.diff(sizes) < 0.0)[0] + 1, [None])
    start, end = 0, 0
    for i, key in enumerate(keys):
      end = indices[i]
      case[key] = {'sizes': sizes[start:end],
                   'data': data[start:end]}
      start = end
  else:
    print('Nothing to store')


def get_data_series(filepaths, key=None, keys=[], skiplines=0):
  series = []
  for filepath in filepaths:
    case = {}
    get_data(case, filepath,
             key=key,
             keys=keys,
             skiplines=skiplines)
    series.append(case)
  return series


def get_average(case, series, key=None, keys=[]):
  if key:
    keys = [key]
  for key in keys:
    case[key] = {'sizes': series[0][key]['sizes'],
                 'data': numpy.array([run[key]['data']
                                      for run in series]).mean(axis=0)}


def get_latency_ratios(case1, case2, key=None):
  ratios = (numpy.array(case1[key]['data']) /
            numpy.array(case2[key]['data']))
  return ratios


def plot_latency_bandwidth(cases, save=None):
  if not type(cases) in [list, tuple]:
    cases = [cases]
  fig, ax = pyplot.subplots(1, 2, figsize=(8.0, 3.0), sharex=True)
  ax[0].grid()
  ax[0].set_xlabel('Message size (bytes)', fontsize=16)
  ax[0].set_ylabel('Point-to-point\nlatency ($\mu$s)', fontsize=16)
  for case in cases:
    ax[0].plot(case['latency']['sizes'], case['latency']['data'],
               label=case['label'],
               linestyle='-', linewidth=1, marker='o', markersize=6)
  ax[0].set_xscale('log')
  ax[0].set_yscale('log')
  ax[1].grid()
  ax[1].set_xlabel('Message size (bytes)', fontsize=16)
  ax[1].set_ylabel('Point-to-point\nbandwidth (MB/s)', fontsize=16)
  for case in cases:
    ax[1].plot(case['bandwidth']['sizes'], case['bandwidth']['data'],
               label=case['label'],
               linestyle='-', linewidth=1, marker='o', markersize=6)
  ax[1].set_xscale('log')
  ax[1].set_yscale('log')
  ax[0].legend(loc='upper left', prop={'size': 14})
  # handles, labels = ax[1].get_legend_handles_labels()
  # fig.legend(handles, labels,
  #            ncol=2, loc='center', prop={'size': 16}, frameon=False,
  #            bbox_to_anchor=(0.54, 0.54))
  fig.tight_layout()
  if save:
    fig.savefig(os.path.join(os.getcwd(), save), dpi=300)


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

pyplot.style.use('seaborn-dark')

case = {'label': 'Azure NC24r'}
keys = ['latency', 'bandwidth']
directory = os.path.join(root_dir, 'run-infiniband')
series = []
for i in range(1, 6):
  tmp_case = {}
  for key in keys:
    filepath = os.path.join(directory, 'nc24r-{}-run{}.log'.format(key, i))
    get_data(tmp_case, filepath, key=key)
  series.append(tmp_case)
get_average(case, series, keys=keys)

common_dir = os.path.join(os.environ['HOME'], 'git', 'mesnardo',
                          'MSAzureGrant', 'runs')

case2 = {'label': 'Azure A9'}
keys = ['latency', 'bandwidth']
directory = os.path.join(common_dir, 'azure-A9cluster', 'osu_benchmarks')
series = []
for i in range(1, 6):
  tmp_case = {}
  for key in keys:
    filepath = os.path.join(directory, 'azurea9-{}-run{}.log'.format(key, i))
    get_data(tmp_case, filepath, key=key)
  series.append(tmp_case)
get_average(case2, series, keys=keys)

case3 = {'label': 'ColonialOne'}
keys = ['bandwidth', 'latency']
directory = os.path.join(common_dir, 'colonialone', 'osu_benchmarks')
series = []
for i in range(0, 5):
  tmp_case = {}
  filepath = os.path.join(directory, 'run{}-openib.log'.format(i))
  get_data(tmp_case, filepath, keys=keys)
  series.append(tmp_case)
get_average(case3, series, keys=keys)

figures_dir = os.path.join(root_dir, 'figures')
if not os.path.isdir(figures_dir):
    os.makedirs(figures_dir)
save_path = os.path.join(figures_dir, 'latencyBandwidthColonialOneAzure.png')
plot_latency_bandwidth([case, case2, case3],
                       save=save_path)
pyplot.show()
