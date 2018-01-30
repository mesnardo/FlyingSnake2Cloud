# Assessing the potential of Microsoft Azure for computational studies of the aerodynamics of animal flight

---

WARNING: this is work in progress.

In 2016, we received a Microsoft Azure Sponsorship with a credit of \$20,000 to use the cloud platform with our in-house Computational Fluid Dynamics software [PetIBM](https://github.com/mesnardo/PetIBM).

PetIBM solves the 2D and 3D Navier-Stokes equations on structured Cartesian grids with an immersed-boundary method.

PetIBM relies on the [PETSc](https://www.mcs.anl.gov/petsc/) library for data structures and parallel routines and run on distributed-memory architectures.
With PetIBM, the user has the possibility to solve the linear systems on CPUs with the PETSc KSP object or on distributed CUDA-capable GPU devices with the [NVIDIA AmgX](https://github.com/NVIDIA/AMGX) library.

We used PetIBM to solve the three-dimensional flow around a cylinder with an anatomically accurate cross-section of a flying snake, the _Chrysopelea paradisi_.
The runs were submitted to Microsoft Azure.

The present repository contains all input files and post-processing scripts used for this study.

---

### Contact

Olivier Mesnard (mesnardo@gwu.edu)
