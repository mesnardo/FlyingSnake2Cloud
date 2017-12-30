## Azure Research Allocations

— [Microsoft Azure for Research Award Program](http://research.microsoft.com/en-us/projects/azure/default.aspx):
 Winning proposals are awarded large allocations of Azure storage and compute resources for one year.

* Deadline: *April 15, 2016*
* Proposal should not exceed 3 pages in length or 1000 words
* Proposal should include resource requirement estimates (number of cores, storage requirements)

*Hardware available for HPC*: Azure A9 nodes have 16 cores and 112GB RAM each, with MPI and Infiniband, measured latency of < 3 µs.
Future release: biggest nodes with 24 CPU cores and 2 x K80 cards (so 4 x GPUs)

#### Proposal Title:
_"Assessing the potential of Azure resources for computational studies of the aerodynamics of animal flight"_

#### Proposal Abstract:
We propose a study to determine suitability and cost/benefit of using Azure cloud for research in computational aerodynamics.
We will run our research code PetIBM to set up a starting condition of the aerodynamic flow around the 3D geometry of a flying snake's body, and run scalability tests on two computational grids: with 45 million and 225 million points, respectively.
For short runs, we will use 2, 4, 8 and 16 nodes (Azure A9) in the first case, and 6, 12, 24 and 48 nodes in the second case.
We also propose to compare the performance obtained on CPU nodes versus GPU nodes, when these become available on Azure.
A total allocation of 200,000 core hours should be enough for completing this study.
We also plan to offer a tutorial at the SciPy conference using pre-loaded Jupyter notebooks, running on Azure cloud.

#### Proposal Narrative:

Our group published a study of the aerodynamics of flying snakes in 2014 [1], using two-dimensional simulations with a fluid solver called cuIBM.
The solver is a serial GPU-enabled code, and thus limited in the size of problems it can handle by the memory available on a single GPU card.
Even so, cuIBM allowed us to find evidence of a surprising aerodynamic effect: enhancement of the lift forces at a particular angle of attack.
Lift-enhancement mechanisms are a major contributor to the flight forces created by animal flyers and gliders, and a source of bioinspiration for robotic air vehicles.
To further this research, our group developed a parallel three-dimensional solver called PetIBM.
It uses the PETSc scientific library to solve systems of algebraic equations in parallel CPU clusters.
Recently, we also coupled PetIBM with the AmgX library for solving systems of equations on multi-GPUs.
This work was presented at the GPU Technology Conference, held April 4-7 2016 in San Jose, CA.
We also made available a technical report as supplementary material to the conference presentation, in the form of a Jupyter notebook:
["Using AmgX to Accelerate PETSc-Based CFD Codes"](http://nbviewer.jupyter.org/github/barbagroup/conferences/blob/2f51957e03585d980a471c52595f46551948b771/GTC2016/GTC2016_S6355.ipynb).
As reported therein, we looked at the cost difference in running simulations with PetIBM on GPU nodes (using AmgX) versus CPU nodes (using PETSc), using AWS EC2 cloud resources.
This was the first time that we studied the suitability of cloud resources for our research, and we are encouraged by the results.

The goal of this Microsoft Azure Research allocation award is to establish the suitability of Azure resources for our research on the aerodynamics of animal flight, using our PetIBM code.
We estimated that with 200k CPU-core hours, we will be able to complete a small-scale study of the parallel performance of PetIBM on Azure CPU nodes.
We would also like to run PetIBM on the new Azure GPU nodes, and compare the time-to-solution and cost of both architectures for our application.
The results of this study will allow us to estimate the resources that would be needed to complete a full study of the three-dimensional lift-enhancement mechanism in anatomically correct sections of a flying snake's body, if we were to use Azure cloud.
With that data, we will suggest a future outlook for moving our research away from university-managed or national-laboratory HPC resources, into cloud.
We will disseminate the results via blog posts, posters and conference presentations at venues like SciPy (Scientific Python Conference), the Supercomputing Conference (SC16) and the International Supercomputing Conference (ISC 2016).

In addition to our focus on research computing on Azure cloud, we have an educational program where we want to take advantage of cloud services.
We are developing a tutorial on high-performance computing with Python and GPUs, using Jupyter Notebooks, for the SciPy conference.
If the new Azure GPU nodes are available by July 2016, we propose to deploy our tutorial on Azure, so that students need not install anything on their personal computers.
This would showcase a new method for teaching large numbers of students using Jupyter Notebooks on cloud-computing resources.

This Azure research effort is in collaboration with Dr. Kenji Takeda, Solutions Architect and Technical Manager for Microsoft Research.

#### Resource requirements estimate

*Problem size:* 
Our prior two-dimensional simulations of the snake cross-section (Krishnan et al., 2014) used a Cartesian stretched grid containing about 2.9 million points.
We centered the body in the domain 30 *c* x 30 *c* (where *c* is the chord-length of the body cross-section).
The grid had a spacing of 0.004*c* in both directions in the near-body region, then stretched with a constant ratio of 1.01 outwards, in each direction.
With the same cross-section grid resolution for the three-dimensional configuration, we can expand the domain in the third direction (spanwise) over a length of π *c*.
Choosing a spanwise cell-width that is 10x larger than cross-section resolution (i.e., 0.04*c*), we end up with a mesh-size of roughly 225 millions points.
This problem size will be our reference to calculate the resource requirements.

The 225-million-point 3D mesh should allow for _direct numerical simulation_ (DNS) of our problem.
But often it is possible to use coarser meshes for an _implicit LES_ (large eddy simulation), without altering averaged forces.
For this reason, we are also interested in testing a 45-million-point mesh obtained by doubling the grid spacing in each direction (while maintaining the same stretching ratio).
This coarse mesh will help us study the scalability of PetIBM and allow us to compare the DNS solution with an implicit-LES solution.

*Memory:* 
A trial run of the three-dimensional problem on a smaller mesh of 4 million points using 4 cores of our lab workstation required 8.8GB of RAM.
We thus estimate that the memory requirements of a PetIBM simulation with a mesh of 225 million points will need a minimum of six Azure A9 nodes (112GB memory each), with a 35% safety factor.
A mesh with 45 million points will fit on two Azure A9 nodes.

*Cost per grid point and time step:* 
A test of 2800 time-steps on a mesh of 10.3 million points took about 36 hours using 1 node (16 hardware cores) of our university cluster. 
That gives an estimated cost per time-step and per mesh-point of $4.5\times10^{-6}$ seconds.

*Experimental setup and compute time:*
In order to perform a strong-scaling study, we propose to run with each mesh over a time-integration period of 100 time-steps with a time-increment giving a CFL number of 0.5 (based on the freestream speed).
That results in a time increment of $4\times10{-3}s$ for the coarser mesh and $2\times10{-3}s$ for the finer mesh.

We will run PetIBM on the coarser mesh to reach the quasi periodic regime of the flow, then interpolate to the finer mesh and restart for another transition period reaching a new quasi periodic regime.
At the end of the first transition stage, we have the starting condition for all the runs with the coarse mesh.
Because this mesh is considerably cheaper to compute, we propose to run a generous period equal to 60 vortex-shedding cycles.
In our previous two-dimensional simulations at Reynolds number 2000, the frequency of shedding was on average 0.375.
Thus, with a time-increment of $4\times10^{-3}$ (corresponding to the coarser mesh), we need to compute 40,000 time-steps, to obtain the solution over 60 vortex-shedding cycles.
This stage will require about 36,000 core hours (FYI: 16x 4.5E-06/3600 x45E+06 x60/0.375/4.0E-03).
For the finer mesh, we will use the end of the second transition stage as a starting condition.
That requires an additional 25 vortex-shedding cycles with time-increment $2\times10^{-3}$.
This will require about 150,000 core hours. (FYI: 16x 4.5E-06/3600 x225E+06 x25/0.375/2.0E-03.)

In sum, most of the required compute resources are needed for the setup of the experiments, with these long runs to reach the quasi-periodic regime. The total requirement is for 186,000 core hours.


*Scaling study:*
We propose a strong-scaling study of PetIBM using the coarser mesh, requesting 2, 4, 8, and 16 nodes. 
Each run will be repeated five times to report the average run time.
For this stage, we estimate a requirement of approximately 1,800 core hours (FYI: 16*4.5E-06/3600*45E+06*100*5*4).
Second, we propose to evaluate the scalability of PetIBM on a DNS-ready mesh size of 225 million points using 6, 12, 24, and 48 nodes.
For this second stage, we estimate a requirement of approximately 9,000 core hours (FYI: 16*4.5E-06/3600*225E+06*100*5*4).

Overall, the estimated resource requirement for the complete study detailed above is 196,800 core hours.

*Comparison with GPU resources:* 
As stated in the introduction, we also developed an AmgX-wrapper, compatible with PetIBM, to solve the linear systems on multiple GPUs.
We propose to compare the performance obtained on CPU nodes versus GPU nodes, when these become available on Azure.
As we don't know when these resources will become available, and cannot anticipate the speed-up that they will provide for our simulation code, we are not including an additional estimate of resources.
Also, from the calculation detailed above, the greater cost comes from the initial run, needed to create a physical starting condition.
Scalability runs are a minor computational cost.

A total allocation of 200,000 core hours should thus be enough for completing this study.

*Future use of Azure cloud*
Our future research goals include a study of the aerodynamic forces of the 3D geometry of a flying snake, at several Reynolds numbers and angles of attack.
Each simulation might require in the order of 100,000 core hours, and we will need to run perhaps a dozen of them.
This Azure research allocation will help us determine the cost-benefits of continuing our research on Azure.

_References_

[1] A. Krishnan, J. Socha, P. Vlachos and L. Barba, "Lift and wakes of flying snakes", Physics of Fluids, vol. 26, no. 3, p. 031901, 2014

