"""
Find appropriate domain limits to crop the numerical solution.
"""

import math
import pathlib
import numpy
import h5py


class Gridline(object):
  def __init__(self, name=None, values=[], filepath=None):
    self.name = name
    self.values = numpy.array(values)
    if filepath:
      self.values = self.read_hdf5(self.name, filepath)

  def read_hdf5(self, name, filepath):
    f = h5py.File(filepath, 'r')
    self.values = f[name][:]
    return self.values

  def get_num_points(self):
    return self.values.size

  def get_bounding_indices(self, xs, xe, tol=1.0E-06):
    mask = numpy.where(numpy.logical_and(self.values >= xs - tol,
                                         self.values <= xe + tol))[0]
    return mask[0], mask[-1]

  def get_limits(self):
    return self.values[0], self.values[-1]

  def get_values(self, indices):
    return self.values[list(indices)]


class Grid(object):
  def __init__(self, name=None, x=None, y=None, z=None, filepath=None):
    self.name = name
    self.x = Gridline(name='x', values=x)
    self.y = Gridline(name='y', values=y)
    self.z = Gridline(name='z', values=z)
    if filepath:
      self.read_hdf5(filepath)
    self.filepath = filepath

  def __repr__(self):
    limits = [round(val, 6) for val in self.get_limits()]
    return ('Grid:\n'
            '  - name: {}\n'
            '  - path: {}\n'
            '  - points: {}\n'
            '  - domain: [{}, {}] x\n'
            '            [{}, {}] x\n'
            '            [{}, {}]\n'
            .format(self.name, self.filepath,
                    ' x '.join([str(n) for n in self.get_num_points()]),
                    *limits))

  def read_hdf5(self, filepath):
    self.x.read_hdf5('x', filepath)
    self.y.read_hdf5('y', filepath)
    self.z.read_hdf5('z', filepath)

  def get_num_points(self):
    return (self.x.get_num_points(),
            self.y.get_num_points(),
            self.z.get_num_points())

  def get_bounding_indices(self, xs, xe, ys, ye, zs, ze, tol=1.0E-06):
    ixs, ixe = self.x.get_bounding_indices(xs, xe, tol=tol)
    iys, iye = self.y.get_bounding_indices(ys, ye, tol=tol)
    izs, ize = self.z.get_bounding_indices(zs, ze, tol=tol)
    return ixs, ixe, iys, iye, izs, ize

  def get_limits(self):
    xs, xe = self.x.get_limits()
    ys, ye = self.y.get_limits()
    zs, ze = self.z.get_limits()
    return xs, xe, ys, ye, zs, ze

  def crop(self, xs, xe, ys, ye, zs, ze, tol=1.0E-06):
    indices = self.get_bounding_indices(xs, xe, ys, ye, zs, ze, tol=tol)
    ixs, ixe, iys, iye, izs, ize = indices
    return Grid(name=self.name + '-crop',
                x=self.x.values[ixs: ixe + 1],
                y=self.y.values[iys: iye + 1],
                z=self.z.values[izs: ize + 1])


# Target sub-domain
xs, xe = -1.0, 6.0
ys, ye = -2.0, 2.0
zs, ze = 0.0, 3.2

script_dir = pathlib.Path(__file__).absolute().parent
root_dir = script_dir.parent

p = Grid(name='p', filepath=root_dir / 'grids/cell-centered.h5')
ux = Grid(name='ux', filepath=root_dir / 'grids/staggered-x.h5')
uy = Grid(name='uy', filepath=root_dir / 'grids/staggered-y.h5')
uz = Grid(name='uz', filepath=root_dir / 'grids/staggered-z.h5')

print(p)
print(ux)
print(uy)
print(uz)

indices = p.get_bounding_indices(xs, xe, ys, ye, zs, ze)
ixs, ixe, iys, iye, izs, ize = indices

p2 = p.crop(*p.x.get_values((ixs, ixe)),
            *p.y.get_values((iys, iye)),
            *p.z.get_values((izs, ize)))
ux2 = ux.crop(*ux.x.get_values((ixs, ixe - 1)),
              *ux.y.get_values((iys, iye)),
              *ux.z.get_values((izs, ize)))
uy2 = uy.crop(*uy.x.get_values((ixs, ixe)),
              *uy.y.get_values((iys, iye - 1)),
              *uy.z.get_values((izs, ize)))
uz2 = uz.crop(*uz.x.get_values((ixs, ixe)),
              *uz.y.get_values((iys, iye)),
              *uz.z.get_values((izs, ize)))

print(p2)
print(ux2)
print(uy2)
print(uz2)

p = 5  # Digit precision to use for the sub-limits
fields = [p2, ux2, uy2, uz2]
dirs = ['x', 'y', 'z']
limits = []
for d in dirs:
  vmin = min([getattr(f, d).values[0] for f in fields])
  limits.append(math.floor(vmin * 10**p) / 10**p)
  vmax = max([getattr(f, d).values[-1] for f in fields])
  limits.append(math.ceil(vmax * 10**p) / 10**p)
print('Sub-limits to use: [{}, {}] x [{}, {}] x [{}, {}]'.format(*limits))
print('For petibm-crop utility:')
print('-x_start {} -x_end {} -y_start {} -y_end {} -z_start {} -z_end {}'
      .format(*limits))
