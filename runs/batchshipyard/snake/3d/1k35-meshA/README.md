# 3D snake, Re=1000, AoA=35deg (mesh A)

---

## Pre-processing steps

### Create the immersed boundary

_Requirements:_
* Python package [snake](https://github.com/mesnardo/snake) (version 0.3).

Create the coordinates of the snake cylinder:
```
python scripts/create-body.py
```

### Create the input file `cartesianMesh.yaml`

_Requirements:_
* Python package [snake](https://github.com/mesnardo/snake) (version 0.3).

Create the input file `cartesianMesh.yaml` that contains the configuration
of the structured Cartesian grid to generate in PetIBM:
```
python scripts/create-cartesianmesh-yaml.py
```

### Get the initial solution from a previous run

_Requirements:_
* [`petibm-utilities`](https://github.com/mesnardo/petibm-utilities); branch `petibm-0.2`.

Get the initial solution by converting the solution obtained after 100000 time
steps from the run at Reynolds number 2000 and angle of attack 35 degrees:
Convert the initial data file from HDF5 to PETSc binary format:
```
scripts/get-initial-conditions.sh
```
The initial conditions are saved in the folder `0100000.org`.
Before running the simulation, rename `0100000.org` into `0100000`.

---

## Run the simulation on Microsoft Azure

Run the simulation.

---

## Post-processing steps

### Convert the velocity field to HDF5 format

_Requirements:_
* [`petibm-utilities`](https://github.com/mesnardo/petibm-utilities); branch `petibm-0.2`.

Convert the velocity from PETSc binary to HDF5 to visualize with VisIt:
```
scripts/convert-velocity.sh
```

Create a XMF file for each component of the velocity field:
```
scripts/createxmf-ux-uy-uz.sh
```

### Compute the vorticity field

_Requirements:_
* [`petibm-utilities`](https://github.com/mesnardo/petibm-utilities); branch `petibm-0.2`.

Compute the streamwise and spanwise components of the vorticity field:
```
scripts/compute-wx-wz.sh
```

Create a XMF file for the x- and z-components of the vorticity field:
```
scripts/createxmf-wx.wz.sh
```


### Plot the vorticity field with VisIt

_Requirements:_
* VisIt (last tested:  2.12.1).
* Python package [snake](https://github.com/mesnardo/snake) (version 0.3).

To plot the 3D contour of the z-component of the vorticity field at saved time steps:
```
sed '1d' flyingSnake3dAoA35.body > postprocessing/snake.p3d
scripts/plot-wz-wake3d-visit.sh
```

To plot the 3D contour of the x- and z-components of the vorticity field at saved time steps:
```
sed '1d' flyingSnake3dAoA35.body > postprocessing/snake.p3d
scripts/plot-wx-wz-wake3d-visit.sh
```

To plot a 2D slice at mid-spanwise of the z-component of the vorticity field at saved time steps:
```
python scripts/create-snake-obj.py
scripts/plot-wz-wake2d-visit.sh
```
