# Microsat-gps-sim
Microsat engineering GNSS simulator


Task Distribution of the assignment for the course Microsat Engineering (AE4S10):
- Create trajectory in csv based on TLE (Bas)
- gps-sdr-sim (Niklas)
- recompile gps-sdr-sim for longer runtimes (done locally, need to check on the machine in the lab) (Niklas)
- run the sdr to gnss receiver and record output in NMEA format (Maurits)
- parse NMEA format (Maurits)
- run the sdr to gnss receiver and record output in binary format (Maurits,Mattias?)
- parse binary format (Maurits,Mattias?)
- write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error (Bas)
- sensitivity to min. elevation angle, ionospheric correction, clock correction, ....., others (Mattias?)


## Create trajectory in csv based on TLE

A trajectory of a satellite can be made with a variety of tools, such as SGP4 or TU Delft's astrodynamics toolbox, called [Tudat](https://docs.tudat.space/en/latest/).
The latter has been chosen for this assignment. One way to propagate a trajectory from initial conditions is via a two line element (TLE) set. These can be obtained for instance from [Celestrak](https://celestrak.org/satcat/search.php) or [Space-track.org](https://www.space-track.org/#catalog). For this assignment the DELFI-PQ has been chosen with NORAD-ID 51074. Either one can be specified to the mentioned webpages to obtain the latest TLE. 

The chosen TLE can be fed to Tudat. Based on included perturbations and other settings, Tudat can propagate the trajectory for a desired time. An example of this is shown in the [trajectory_generation folder](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/Code/simulation.py). 
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

Since the frequency of the gps-sdr-sim software is 10 Hz, a fixed step size of 0.1 s has been used in the Tudat simulation. Contrary to the GNSS receiver, the propagation time of Tudat is not limited by the actual duration of the propagation. In fact, trajectories of days or months are generated within seconds or at most a few minutes, when using the modest step size of 0.1 s and an rk4 integrator. 

The propagation results of Tudat are stored in the state history, containing the inertial position and velocity components. Moreover, any dependent variables of interest can be stored. The latter is one of the main reasons why Tudat has been chosen. By saving the following dependent variables in csv format:

- longitude, latitude, altitude
- position and velocity components in the earth centered earth fixed (ECEF) frame
- Keplerian states

no additional computations have to be performed to transform the inertial position and velocity to these states. 

## gps-sdr-sim 


Once the files containing the xyz or llh position information are generated, the signals to be replayed by the SDR to the GNSS receiver can be generated. For this purpose, the open-source software gps-sdr-sim is used. 

At the start of the project, however, a few issues were encountered. The motion data that is input when running the software is stored in a 2D-array, which has a size that is defined by a value set at compile time. Thus, the precompiled executable that exists in the repository cannot be used for simulations longer than 5 minutes, as that is the default value for the size of that array. Thus, a compiler was installed, the flag changed to a value allowing a simulation of at least a few orbits and the program recompiled. 

At this point another issue was discovered in the form of a bug that occurs when running the program if it has been compiled using a long maximum runtime parameter. This bug stopped the program from running at all, immediately causing a segmentation fault upon execution. After some debugging the cause was found to be a stackoverflow due to how the previously mentioned 2D-array was declared inside of the main function. With large runtimes this array consumed large amounts of memory on the stack, exceeding the available space in the stack. This has been fixed by simply moving the declaration of that array outside of the main function, such that it would not be allocated on the stack, thus making a stackoverflow due to this reason impossible. The fix was first implemented locally and tested, and once proved successful a [pull-request](https://github.com/osqzss/gps-sdr-sim/pull/389) on the public repository was created and successfully merged. 

Now it was possible to generate the desired signals for two orbits and replay them to the receiver, which worked good at first. However, it was noticed that the receiver would periodically lose lock and not recover quickly. It was observed on the Receiver GUI that commanding a hot restart would quickly regain a fix. Thus a program was written that would record all the data from the receiver for later analysis, while checking at all times whether a position fix is present. If the fix is lost, it issues the hot restart command. Doing this reduced the outage time from a large fraction of the two orbit run down to below 90 seconds over the two orbits with a total duration of a bit over three hours.

To summarize the workflow to make this reproducible here:

- recompile gps-sdr-sim with a large USER_MOTION_SIZE parameter (desired simulation time in seconds times 10): 
```
$ gcc gpssim.c -lm -O3 -o gps-sdr-sim.exe -DUSER_MOTION_SIZE=98000
```
- generate signal file using gps-sdr-sim and brdc file (we used the default one in the repository, attention the output file is very large being about 1GB per 100s of simulation):
```
$ gps-sdr-sim.exe -e <brdc file> -u/-x <motion-file in either ECEF xyz (-u) or LLH (-x)> -s 2600000 -o <output file location/name>
```

- now replay the generated output file to the SDR using the python script provided in the repository (requires a few conda packages):
```
$ python gps-sdr-sim-uhd.py -t <output file previously generated> -s 2600000 -x 30 
```
- now the sdr will transmit the simulated gps signals, and the receiver will start being able to generate a fix. Thus we will (in a seperate window) run the recording and hot-restart program located in the recording folder of this repository:
```
$ python NMEA_store.py
```

Now the simulation will run in an infinite loop, with the transmission restarting once it is done. Thus, once the generated signal has been completely transmitted both programs need to be manually stopped (Ctrl+C), leaving a log file with a timestamp of all NMEA messages the receiver has generated. 



## Run the sdr to gnss receiver and record output in NMEA format

................


## Parse NMEA format

................


## Run the sdr to gnss receiver and record output in binary format

................


## Parse binary format


................


## Write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error of the GNSS receiver with respect to the benchmark trajectory

Based on the benchmark trajectory and the GNSS receiver output, the GNSS receiver error can be quantified. This can be done in various ways. The following errors have been analyzed:

- state error in the ECEF frame
- radial (R), along track (S), cross track (W) error in the RSW frame
- error in the Keplerian elements

These errors are commonly analyzed in astrodynamics. 

The state error in the ECEF frame has been directly calculated by taking the difference in ECEF state components between the benchmark trajectory and the GNSS receiver. The state error in the ECEF frame is shown in the following figure:


not the actual error plots!!!!!!!!!!!!!!!!!!!!!!!!!!

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/6fe12c6a-d308-44f1-b6da-bc8a003addc5" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/bc6c2f6e-f9ce-4dcb-b991-7eb3d6e0e44b" alt="Image 2"></td>
  </tr>
</table>

As can be observed from the figures, the order of magnitude of the error of the position components is ... m. For the velocity components, the order of magnitude of the error is ... m/s.


............................


To charachterize the radial, along track, cross track error in the RSW frame, further clarification is required. Depending on the orientation and location of the satellite with respect to the earth, the RSW coordinate system which is attached to the satellite differs. Consequently, to calculate the radial, along track and cross track error, one satellite has to be taken as the reference. As the benchmark trajectory is considered to be the truth, the RSW frame to quantify the error is fixed to the satellite of the benchmark trajectory. The radial, along track and cross track components of the benchmark trajectory can be calculated by converting its inertial components to RSW components. This can be done by multipliying the [inertial to RSW transformation matrix](https://py.api.tudat.space/en/stable/frame_conversion.html#tudatpy.astro.frame_conversion.inertial_to_rsw_rotation_matrix) with the inertial position. The inertial to RSW transformation matrix also requires the inertial position itself to compute the orientation of the frame. The radial, along track and cross track components of the GNSS receiver with respect to this frame can be calculated by multiplying the same inertial to RSW transformation matrix, still with the inertial benchmark trajectory as input, with the inertial components of the GNSS receiver. 

The radial, along track and cross track error in the RSW frame is shown in the following figure:


not the actual error plots!!!!!!!!!!!!!!!!!!!!!!!!!!

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/1afed979-c901-4242-bd14-cefe7c5dcee9" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/81620b59-0f74-420f-8212-9969501c9afb" alt="Image 2"></td>
  </tr>
</table>

For the position components in the RSW frame, it is observed that the order of magnitude of the radial error is ... m. For the along track direction, the order of magnitude of the error is ...m. Finally, the cross-track direction has the smallest error. Its order of magnitude is ...m. 

For the velocity components in the RSW frame, it is observed that the order of magnitude of the radial error is ... m/s. For the along track direction, the order of magnitude of the error is ...m/s. Finally, the cross-track direction has the smallest error. Its order of magnitude is ...m/s. 




............................



The error in the Keplerian elements is shown in the following figure:


not the actual error plots!!!!!!!!!!!!!!!!!!!!!!!!!!

![image](https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/a6ba62e2-dc6c-41dd-8ecf-01c913ad1e08)


The following observations are made from the evolution of the error of the six Keplerian elements. 

............................





