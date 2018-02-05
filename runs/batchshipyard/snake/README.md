# Flying-snake simulations on Microsoft Azure using Batch service and Batch Shipyard

---

## Directory contents

- `2d`: two-dimensional runs
    + `2k35`: Re=2,000 and AoA=35 deg (3-million-cell grid)
    + `configs`: Batch Shipyard configuration files
- `3d`: three-dimensional runs
    + `1k35-meshA`: Re=1,000 and AoA=35 deg (46-million-cell grid)
    + `2k30-meshA`: Re=2,000 and AoA=30 deg (46-million-cell grid)
    + `2k35-meshA`: Re=2,000 and AoA=35 deg (46-million-cell grid)
    + `2k35-meshB`: Re=2,000 and AoA=35 deg (233-million-cell grid)
    + `2k35-meshB-restart1`: Re=2,000 and AoA=35 deg (233-million-cell grid); first restart
    + `2k35-meshB-restart2`: Re=2,000 and AoA=35 deg (233-million-cell grid); second restart
    + `configs`: Batch Shipyard configuration files
    + `scripts`: Python post-processing scripts
- `data`: force coefficients obtained with 2D PetIBM simulations
- `docker`: Docker files to create a Docker image of PetIBM in optimized mode
- `docker-dbg`: Docker files to create a Docker image of PetIBM in debugging mode

## Software versions

- PetIBM (tag "0.2-noversionchecks")
- PETSc-3.7.4
- AmgX-2.0.0-public-build125
- Intel MPI-5
- CUDA-8.0