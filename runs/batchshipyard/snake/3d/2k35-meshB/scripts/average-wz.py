"""
Average the spanwise vorticity field along the spanwise direction and write the
2D field values into HDF5 file.
"""

import pathlib
import numpy
import h5py


def read_grid3d_hdf5(filepath):
  f = h5py.File(str(filepath), 'r')
  x, y, z = f['x'][:], f['y'][:], f['z'][:]
  f.close()
  return x, y, z


def write_grid2d_hdf5(x, y, filepath):
  f = h5py.File(str(filepath), 'w')
  f.create_dataset('x', data=x)
  f.create_dataset('y', data=y)
  f.close()


def read_data_hdf5(filepath, name):
  f = h5py.File(str(filepath), 'r')
  data = f[name][:]
  f.close()
  return data


def write_data_hdf5(data, filepath, name):
  f = h5py.File(str(filepath), 'w')
  f.create_dataset(name, data=data)
  f.close()


script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent
data_dir = root_dir / 'postprocessing/vorticity-crop'
out_dir = data_dir / 'spanwise-average'

variable_names = ['wz']
timesteps = list(range(102400, 198400 + 1, 3200))
for name in variable_names:
  print('Variable: {}'.format(name))
  # Read the 3D grid from HDF5 file.
  filepath = data_dir / 'grids/{}.h5'.format(name)
  x, y, _ = read_grid3d_hdf5(filepath)
  # Write a 2D slice into HDF5 file.
  filepath = out_dir / 'grids/{}.h5'.format(name)
  filepath.parent.mkdir(parents=True, exist_ok=True)
  write_grid2d_hdf5(x, y, filepath)
  # Loop over the saved time-steps.
  for timestep in timesteps:
    print('[time-step {}]'.format(timestep))
    # Read the 3D field data from HDF5 file.
    filepath = data_dir / '{:0>7}/{}.h5'.format(timestep, name)
    data = read_data_hdf5(filepath, name)
    # Compute the mean along the spanwise direction.
    data_mean = numpy.mean(data, axis=0)
    # Write the 2D field data into HDF5 file.
    filepath = out_dir / '{:0>7}/{}.h5'.format(timestep, name)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    write_data_hdf5(data_mean, filepath, name)
