# Microsat-gps-sim
Microsat Engineering GNSS simulator


Task Distribution of the assignment for the course Microsat Engineering (AE4S10):
- Create trajectory in csv based on TLE (Bas)
- gps-sdr-sim (Niklas)
- recompile gps-sdr-sim for longer runtimes (done locally, need to check on the machine in the lab) (Niklas)
- commanding and communicating with GNSS (Maurits)
- run the sdr to gnss receiver and record output in NMEA format (Maurits)
- parse NMEA format (Maurits)
- run the sdr to gnss receiver and record output in binary format (Maurits)
- parse binary format (Maurits)
- facilitation from parsed data to usable units and desired structure of data, both Binary and NMEA (Mattias)
- write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error (Bas)
- sensitivity analysis (Bas)



## Create trajectory in csv based on TLE

A trajectory of a satellite can be made with a variety of tools, such as SGP4 or TU Delft's astrodynamics toolbox, called [Tudat](https://docs.tudat.space/en/latest/).
The latter has been chosen for this assignment. One way to propagate a trajectory from initial conditions is via a two line element (TLE) set. These can be obtained for instance from [Celestrak](https://celestrak.org/satcat/search.php) or [Space-track.org](https://www.space-track.org/#catalog). For this assignment the DELFI-PQ has been chosen with NORAD-ID 51074. Either one can be specified to the mentioned webpages to obtain the latest TLE. 

The chosen TLE can be fed to Tudat. Based on included perturbations and other settings, Tudat can propagate the trajectory for a desired time. An example of this is shown in the [trajectory_generation folder](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/Code%20for%20Delfi-PQ/simulation.py). 
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

The propagation results of Tudat are stored in the state history, containing the inertial position and velocity components. Moreover, any dependent variables of interest can be stored. The latter is one of the main reasons why Tudat has been chosen. The following dependent variables are stored:

- longitude, latitude, altitude in the earth centered earth fixed (ECEF) frame
- position and velocity components in the earth centered earth fixed (ECEF) frame
- Keplerian states

The ground track of Delfi-PQ and the altitude profile are shown below:

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/a6093c9f-8da0-43bc-9c8b-f769eb2b6d74" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/a8ced585-90d5-40e1-bea2-64feaa87dfae" alt="Image 2"></td>
  </tr>
</table>


As can be seen, the benchmark and GNSS values are overlapping, which is one of the verification checks which have been performed.

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

## Commanding the GNSS 

For this assignment commanding the GNSS was required to achieve the desired results, those being: change of output (between NMEA and Binary) and elevation (query and changing). In addition, a variable-size answer code was made to ensure that the exact size of the answer to any command is received (determined by receiving the payload size hex, which is the only section of the message of variable size, allowing to determine the full size of the answer) without missing anything or "reading" more than needed. The commands are present in the "general_commands.py" and the query for the command choice is present.


## Run the sdr to gnss receiver and record output in NMEA format

To retrieve the data from the simulation with the NMEA output a few actions must be taken. First the GNSS needs to be commanded to output in NMEA (where the code will ask which command is desired to be sent), secondly the NMEA output recorder is engaged and finally the RF signals are fed into the SDR. Then the desired time needs to be waited while the simulation is run:

- Step 1:
```
$ python general_commands.py
```
- Step 1.1:
- - Answer: NMEA
- Step 2:
```
$ python NMEA_store.py
```
- Step 3:
```
$ python gps-sdr-sim-uhd.py -t <output file previously generated> -s 2600000 -x 30 
```

## Parse NMEA format

Having the saved file with the output, it was necessary to translate it into useful data. For the first step, it is used the NMEA parser (found in parsing_NMEA.py) to translate the data into decimal values for each parameter with its label and unit. Then following the first step the data is again translated (present in ...........py) into the desired units and outputted into a specific order to execute the analysis. The separation of the action was done so to avoid the possibility of error and for easier error detection by evaluating the interim outputs.

## Run the sdr to gnss receiver and record output in binary format

To retrieve the data from the simulation with the BINARY output a few actions must be taken. First the GNSS needs to be commanded to output in NMEA (where the code will ask which command is desired to be sent), secondly the NMEA output recorder is engaged and finally the RF signals are fed into the SDR. Then the desired time needs to be waited while the simulation is run:

- Step 1:
```
$ python general_commands.py
```
- Step 1.1:
- - Answer: BINARY
- Step 2:
```
$ python BINARY_store.py
```
- Step 3:
```
$ python gps-sdr-sim-uhd.py -t <output file previously generated> -s 2600000 -x 30 
```

## Parse binary format

Having the output files from the Binary it is saved as hex per line. Therefore, it is required to translate from hex to decimal and separate per component (which is explained in https://www.skytraq.com.tw/homesite/AN0037.pdf) which is executed in binary_parsing.py. After such action is taken another translation is done where the units of the data points are standardized and outputs only the desired components of the data points useful for the analysis. As specified in the NMEA parsing all the different actions are taken separately for easier error detection by the evaluation of the interim outputs.

## Facilitation from parsed data to usable units and desired structure of data, both Binary and NMEA
The parsed data is not in the desired format yet and needs to be transformed in order to be useful. Only ten variables were if interest for the error analysis; time, longitude, latitude, altitude, x-position, y-position, z-position, x-speed, y-speed and z-speed. The following actions were performed for the data:

For the NMEA:
- First the time of first lock is estabilished
- Then the time is converted form UTC to seconds and 18 leap seconds are added to account for conversion of gps datetime
- All data before first lock is deleted (as there is no useful data)
- A .txt file is created with 4 columns; time, longitude, latitude, altitude
- Afterwards a post processing code removes duplicate and ensures that every entry in the four columns is complete

For the Binary:
- As converting the output of the binary data into a .txt file sometimes erronously creates a new line, the raw binary output is preprocessed to ensure there are no mistakes and every line is a complete message (This issue had been FIXED, so the prepocessing is not necessary anymore)
- Afterwards the time of first lock is estabilished
- Then the time is converted form UTC to seconds
- All data before first lock is deleted (as there is no useful data)
- A .txt file is created with 7 columns; time, x, y, z, vx, vy, vz

There were many bugs when trying to automate the binary processing. As such a manual code is in the processing folder. Here the user only has to input the to be processed file name and specify the output name. The file will be saved in the same folder.

## Write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error of the GNSS receiver with respect to the benchmark trajectory

Based on the benchmark trajectory and the GNSS receiver output, the GNSS receiver error can be quantified. This can be done in various ways. The following errors have been analyzed:

- state error in the ECI frame
- radial (R), along track (S), cross track (W) error in the RSW frame
- error in the Keplerian elements
- RMS error of the position and velocity

These errors are commonly analyzed in astrodynamics. All errors are programmatically obtained by running the [run simulation file](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/Code%20for%20Delfi-PQ/run_simulation.py). 
Before analyzing them, the theoretical accuracy of the [S1216F8-GI3 GPS receiver](https://www.skytraq.com.tw/datasheet/S1216V8_v0.9.pdf) is reported to be:

- position accuracy: 2.5 m CEP (Circular Error Probability)
- velocity accuracy: 0.1 m/s
- time accuracy: 10 ns

To calculate the state error in the ECI frame, the ECEF states of the GNSS output are converted to ECI states through the [body fixed to inertial transformation](https://py.api.tudat.space/en/latest/environment.html#tudatpy.numerical_simulation.environment.RotationalEphemeris.body_fixed_to_inertial_rotation).
The state error in the ECI frame can then be calculated by taking the difference in ECI state components between the benchmark trajectory and the GNSS receiver. The state error in the ECI frame is shown in the following figure:


<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/e8f3e320-96ee-437f-99db-5e4f69e7fc4e" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/02380160-b588-4305-b391-607fa1c1890c" alt="Image 2"></td>
  </tr>
</table>



As can be observed from the figures, the order of magnitude of the error of the position components is ... m. For the velocity components, the order of magnitude of the error is ... m/s. 

While the error in the state components gives a rough idea of the order of magnitude of the error, a metric for the overall error would be even more useful, as the error in the x, y and z components depends largely on the inclination of the orbit. The root mean squared error (RMSE) gives a good indication of the overall error, which can be also be readily compared with other orbits with different inclination. 

The RMSE calculated up to any time in the propagation is shown in:

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/7f6e165a-adf7-44de-91a0-1c9b94980426" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/2fa2d3e8-811b-40a2-8da8-05041d4b157c" alt="Image 2"></td>
  </tr>
</table>


At the final propagation time, after two full orbits, the RMSE is ... m for the position and ... m/s for the velocity. This is ......


To charachterize the radial, along track, cross track error in the RSW frame, further clarification is required. Depending on the orientation and location of the satellite with respect to the earth, the RSW coordinate system which is attached to the satellite differs. Consequently, to calculate the radial, along track and cross track error, one satellite has to be taken as the reference. As the benchmark trajectory is considered to be the truth, the RSW frame to quantify the error is fixed to the satellite of the benchmark trajectory. The radial, along track and cross track components of the benchmark trajectory can be calculated by converting its inertial components to RSW components. This can be done by multipliying the [inertial to RSW transformation matrix](https://py.api.tudat.space/en/stable/frame_conversion.html#tudatpy.astro.frame_conversion.inertial_to_rsw_rotation_matrix) with the inertial position. The inertial to RSW transformation matrix also requires the inertial position itself to compute the orientation of the frame. The radial, along track and cross track components of the GNSS receiver with respect to this frame can be calculated by multiplying the same inertial to RSW transformation matrix, still with the inertial benchmark trajectory as input, with the inertial components of the GNSS receiver. 

The radial, along track and cross track error in the RSW frame is shown in the following figure:

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/66ffd4c0-d66d-48af-9f1c-74d95c664294" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/7f252221-aa3b-4846-b8fb-ba4fef4dedb9" alt="Image 2"></td>
  </tr>
</table>

For the position components in the RSW frame, it is observed that the order of magnitude of the radial error is ... m. For the along track direction, the order of magnitude of the error is ...m. Finally, the cross-track direction has the smallest error. Its order of magnitude is ...m. 

For the velocity components in the RSW frame, it is observed that the order of magnitude of the radial error is ... m/s. For the along track direction, the order of magnitude of the error is ...m/s. Finally, the cross-track direction has the smallest error. Its order of magnitude is ...m/s. 


The error in the Keplerian elements is shown in the following figure:


![image](https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/a6ba62e2-dc6c-41dd-8ecf-01c913ad1e08)


The following observations are made from the evolution of the error of the six Keplerian elements:





## Sensitivity analysis

It has also been investigated which settings can be changed to get the error down further. These were motivated by factors which have been analyzed in the [paper](https://www.sciencedirect.com/science/article/pii/S0273117723008050).
These factors are: 

- ionospheric refraction, as influenced by the min. elevation angle. 
- insufficient dynamic model lacking for instance Coriolis and centrifugal acceleration
- antenna location

The sensitivity analysis has been carried out in the [sensitivity analysis folder](https://github.com/niklasknoell/Microsat-gps-sim/tree/Bas/trajectory_generation/sensitivity%20analysis). To enable automation, a user only has to choose a [name of the sensitivity simulation](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/sensitivity%20analysis/choose_simulation.py) of interest and run the [run simulation file](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/sensitivity%20analysis/run_simulation.py), which will run all code in the right order. 


The ionospheric refraction has been tested by .....


It was found that ...... indeed enable to get a lower error. Incorporating .... this gives the following error plots, which after comparison with the previous error plots indeed shows that the error can be reduced. 


The second factor of the paper, a possibly insufficient dynamic model, could not be tested as the dynamic model of the GNSS could not be altered. 
Moreover, the influence of the antenna location could not be tested, because while the receiver is orbiting on a virtual trajectory, it is not attached to an actual satellite, and is not obstructed by its satellite body. 


  
  







