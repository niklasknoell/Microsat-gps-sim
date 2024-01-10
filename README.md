# Microsat-gps-sim
Microsat engineering GNSS simulator


Task Distribution:
- Create trajectory in csv based on TLE (Bas)
- gps-sdr-sim (Niklas)
- recompile gps-sdr-sim for longer runtimes (done locally, need to check on the machine in the lab) (Niklas)
- run the sdr to gnss receiver and record output in NMEA format (Maurits)
- parse NMEA format (Maurits)
- run the sdr to gnss receiver and record output in binary format (Maurits,Mattias?)
- parse binary format (Maurits,Mattias?)
- write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error (Bas)


## Create trajectory in csv based on TLE

A trajectory of a satellite can be made with a variety of tools, such as SGP4 or TU Delft's astrodynamics toolbox, called [Tudat](https://docs.tudat.space/en/latest/).
The latter has been chosen for this assignment. One way to propagate a trajectory from initial conditions is via a two line element (TLE) set. These can be obtained for instance from [Celestrak](https://celestrak.org/satcat/search.php) or [Space-track.org](https://www.space-track.org/#catalog). For this assignment the DELFI-PQ has been chosen with NORAD-ID 51074. Either one can be specified to the mentioned webpages to obtain the latest TLE. 

The chosen TLE can be fed to Tudat. Based on included perturbations and other settings, Tudat can propagate the trajectory for a desired time. An example of this is shown in the trajectory_generation folder of this repository, under simulation.py. 
As the trajectory from Tudat is to be used as a benchmark, considered as the truth, the model should be accurate enough to quantify the order of magnitude of the error of the GNSS receiver with respect to this benchmark. To this end, the following perturbations are included in the simulation:

- Earth spherical harmonic gravity to degree and order five (5,5)
- Aerodynamic drag
- Sun point mass gravity
- Sun cannonball radiation pressure
- Moon point mass gravity

The aerodynamic drag and the radiation pressure from the sun require the following inputs:

- drag reference area of 5x5x18 cm
- drag coefficient
- radiation reference area of 5x5x18 cm
- radiation coefficient

The drag and radiation reference area have been calculated based on the satellite dimensions, which are 5x5x18 cm for Delfi-PQ. The drag and radiation coefficient have both been assumed to be 1.2, which is in line with values used for the slighly larger 3U Delfi-C3 on [Tudat](https://docs.tudat.space/en/latest/_src_getting_started/_src_examples/notebooks/propagation/linear_sensitivity_analysis.html). 

Since the frequency of the GNSS receiver is 10 Hz, a fixed step size of 0.1 s has been used in the Tudat simulation. Contrary to the GNSS receiver, the propagation time of Tudat is not limited by the actual duration of the propagation. In fact, trajectories of days or months are generated within seconds or at most a few minutes, when using the modest step size of 0.1 s and an rk4 integrator. 

The propagation results of Tudat are stored in the state history, containing the inertial position and velocity components. Moreover, any dependent variables of interest can be stored. The latter is one of the main reasons why Tudat has been chosen. By saving the following dependent variables in csv format:

- longitude, latitude, altitude
- position and velocity components in the earth centered earth fixed (ECEF) frame
- Keplerian states

no additional computations have to be performed to transform the inertial position and velocity to these states. 

## gps-sdr-sim 


.......





## Write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error of the GNSS receiver with respect to the benchmark trajectory. 

Based on the benchmark trajectory and the GNSS receiver output, the GNSS receiver error can be quantified. This can be done in various ways. The following errors have been analyzed:

- state error in the ECEF frame
- radial (R), along track (S), cross track (W) error in the RSW frame
- error in the Keplerian elements

These errors are commonly analyzed in astrodynamics. 

The state error in the ECEF frame has been directly calculated by taking the difference in ECEF state components between the benchmark trajectory and the GNSS receiver. The state error in the ECEF frame is shown in the following figure:


............................


To charachterize the radial, along track, cross track error in the RSW frame, further clarification is required. Depending on the orientation and location of the satellite with respect to the earth, the RSW coordinate system which is attached to the satellite differs. Consequently, to calculate the radial, along track and cross track error, one satellite has to be taken as the reference. As the benchmark trajectory is considered to be the truth, the RSW frame to quantify the error is fixed to the satellite of the benchmark trajectory. The radial, along track and cross track components of the benchmark trajectory can be calculated by converting its inertial components to RSW components. This can be done by multipliying the [inertial to RSW transformation matrix](https://py.api.tudat.space/en/stable/frame_conversion.html#tudatpy.astro.frame_conversion.inertial_to_rsw_rotation_matrix) with the inertial position itself. The inertial to RSW transformation matrix also requires the inertial position itself to compute the orientation of the frame. The radial, along track and cross track components of the GNSS receiver with respect to this frame can be calculated by multiplying the same inertial to RSW transformation matrix, still with the inertial benchmark trajectory as input, with the inertial components of the GNSS receiver. 

The radial, along track and cross track error in the RSW frame is shown in the following figure:


............................



The error in the Keplerian elements is shown in the following figure:



............................



