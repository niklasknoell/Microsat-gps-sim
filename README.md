# Microsat-gps-sim
Microsat Engineering GNSS simulator


Task Distribution of the assignment for the course Microsat Engineering (AE4S10):
- Create trajectory in csv based on TLE (Bas)
- gps-sdr-sim (Niklas)
- recompile gps-sdr-sim for longer runtimes (Niklas)
- commanding and communicating with GNSS (Maurits)
- run the sdr to gnss receiver and record output in NMEA format (Maurits)
- parse NMEA format (Maurits)
- run the sdr to gnss receiver and record output in binary format (Maurits)
- parse binary format (Maurits)
- facilitation from parsed data to usable units and desired structure of data, both binary and NMEA (Mattias)
- write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error of the GNSS receiver (Bas)
- sensitivity analysis (Bas)



## Create trajectory in csv based on TLE

A trajectory of a satellite can be made with a variety of tools, such as SGP4 or TU Delft's astrodynamics toolbox, called [Tudat](https://docs.tudat.space/en/latest/).
The latter has been chosen for this assignment. One way to propagate a trajectory from initial conditions is via a two line element (TLE) set. These can be obtained for instance from [Celestrak](https://celestrak.org/satcat/search.php) or [Space-track.org](https://www.space-track.org/#catalog). For this assignment the DELFI-PQ has been chosen with NORAD-ID 51074. Either one can be specified to the mentioned webpages to obtain the latest TLE. 

The chosen TLE can be fed to Tudat. Based on included perturbations and other settings, Tudat can propagate the trajectory for a desired time. An example of this is shown in the [trajectory_generation folder](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/Code%20for%20Delfi-PQ/simulation.py). 
As the trajectory from Tudat is to be used as a benchmark, considered as the truth, the model should be accurate enough to quantify the error of the GNSS receiver with respect to this benchmark. To this end, the following perturbations are included in the simulation:

- earth spherical harmonic gravity to degree and order five (5,5)
- aerodynamic drag
- sun point mass gravity
- sun cannonball radiation pressure
- moon point mass gravity

The aerodynamic drag and the radiation pressure from the sun require the following inputs:

- drag reference area 
- drag coefficient
- radiation reference area 
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


As can be seen, the benchmark and GNSS values are overlapping, which is one of the verification checks which have been performed. In the above two figures, the GNSS curve has been made with the longitude, latitude and altitude returned by the NMEA parser. Only two small periods without GNSS lock can be seen, which is considered relatively good for a period of about 3 hrs. 

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

## Write analysis program to compare trajectory input and GNSS receiver output, i.e. quantify error of the GNSS receiver

Based on the benchmark trajectory and the GNSS receiver output, the GNSS receiver error can be quantified. This can be done in various ways. The following errors have been analyzed:

- state error in the ECI frame
- radial (R), along track (S), cross track (W) error in the RSW frame
- error in the Keplerian elements
- RMS error of the position and velocity
- 3D error of position and velocity

These errors are commonly analyzed in astrodynamics. All errors are programmatically obtained by running the [run simulation file](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/Code%20for%20Delfi-PQ/run_simulation.py). 
Before analyzing them, the theoretical accuracy of the [S1216F8-GI3 GPS receiver](https://www.skytraq.com.tw/datasheet/S1216V8_v0.9.pdf) is reported to be:

- position accuracy: 2.5 m CEP (Circular Error Probability)
- velocity accuracy: 0.1 m/s
- time accuracy: 10 ns


Furthermore, another important remark should be made, which is that the following figures have been cut off after about 40 min, which is the time until the first loss of lock, for the particular simulation analyzed. This does mean that not the full patterns over an orbit can be observed. 

To calculate the state error in the ECI frame, the ECEF states of the GNSS output are converted to ECI states through the [body fixed to inertial transformation](https://py.api.tudat.space/en/latest/environment.html#tudatpy.numerical_simulation.environment.RotationalEphemeris.body_fixed_to_inertial_rotation).
The state error in the ECI frame can then be calculated by taking the difference in ECI state components between the benchmark trajectory and the GNSS receiver.

The state error in the ECI frame is shown in the following figure:

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/04d4058c-1bc5-41e2-bf50-750df5e98538" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/49e22047-f455-42a6-a3a4-4d3ce864500a" alt="Image 2"></td>
  </tr>
</table>



As can be observed from the figures, the error of the position components is several tens of meter. For each velocity component, the error is mostly within 0.1 m/s. 
Moreover, while the GNSS simulation has been allowed to be longer than 300 sec, a jump in the position components is induced after every 300 seconds. This is to be disregarded and has not a physical reason. 


While the error in the state components give a rough idea of the order of magnitude of the error, a metric for the overall error would be even more useful, as the error in the x, y and z components depends largely on the inclination of the orbit. The root mean squared error (RMSE) gives a good indication of the overall error, which can also be readily compared with other orbits with different inclination. Moreover, the 3D error of position and velocity is chosen for direct comparison against the theoretical accuracy.

The RMSE and 3D error, calculated up to any time in the propagation, are shown below:

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/f03f5111-6b5f-47cc-8e6f-242038e70101" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/028ec802-db76-4ed5-a051-fdef601c7fc5" alt="Image 2"></td>
  </tr>
</table>


The RMSE of the postion and the 3D position error is about 70 m. This is signficantly higher than the theoretical 2.5 m CEP. However, no corrections have been made yet to the settings used for the GNSS simulation. It is expected that the position error can be reduced further by incorporating corrections in the equation for the pseudo-range. The 3D velocity error is approximately 0.1 m/s, which is in line with the theoretical accuracy. 

To charachterize the radial (R), along track (S), cross track (W) error in the RSW frame, further clarification is required. Depending on the orientation and location of the satellite with respect to the earth, the RSW coordinate system which is attached to the satellite differs. Consequently, to calculate the radial, along track and cross track error, one satellite has to be taken as the reference. As the benchmark trajectory is considered to be the truth, the RSW frame to quantify the error is fixed to the satellite of the benchmark trajectory. The radial, along track and cross track components of the benchmark trajectory can be calculated by converting its inertial components to RSW components. This can be done by multipliying the [inertial to RSW transformation matrix](https://py.api.tudat.space/en/stable/frame_conversion.html#tudatpy.astro.frame_conversion.inertial_to_rsw_rotation_matrix) with the inertial position. The inertial to RSW transformation matrix also requires the inertial position itself to compute the orientation of the frame. The radial, along track and cross track components of the GNSS receiver with respect to this frame can be calculated by multiplying the same inertial to RSW transformation matrix, still with the inertial benchmark trajectory as input, with the inertial components of the GNSS receiver. 

The radial, along track and cross track error in the RSW frame is shown in the following figure:

<table>
  <tr>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/07be6622-9f73-4ef4-a139-e8f28e56f17f" alt="Image 1"></td>
    <td><img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/25225f44-4f04-4804-841f-3c0848700454" alt="Image 2"></td>
  </tr>
</table>

For the position components in the RSW frame, it is observed that the error of the along track (S) direction is about 70 m. Besides, it has the largest error of all components. Moreover, from this plot it can be observed that the periodic jump in error after every 300 sec, is dominant in the along track (S) component.
The radial (R) error is oscillating about a mean of about 2 m. Finally, the error in the cross-track (W) direction is also oscillating, but with a much larger period. Is is unknown whether the Coriolis acceleration is incorporated in the dynamic model. However from literature, neglecting this acceleration is known to cause a periodic error (with period equal to the orbital period) in the cross-track (W) direction for a polar orbit, which Delfi-PQ has. Therefore, it is hypothesized that the Coriolis acceleration has indeed been neglected in the dynamic model. 



A clear jump in radial error due to close proximity to the total electron content (TEC) maximum has not been observed. Most likely, for the 90 min orbital period of Delfi-PQ, the analyzed simulation of 40 min has not passed the (TEC) maximum. It is expected that for longer simulations the spike in radial error will arise due to the guarantee that somewhere during the orbit, the closest point to the (TEC) maximum will be passed. 

For the velocity components in the RSW frame, it is observed that the radial (R) error is mostly under 0.1 m/s, which is about twice as large as the along-track (S) and cross-track (W) direction. 

The error in the Keplerian elements is shown in the following figure:


![image](https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/096d14be-b749-40fc-9709-1c6c719f3626)

In the inclination and RAAN, some sort of periodic bias is present, which would be expected when the Coriolis acceleration would have been neglected in the dynamic model. However again, more simulations with a longer runtime would have to be performed to better assess this. Therefore, one strong recommendation for improvement based on the presented work is to alter the binary parser such that the GNSS lock is never lost.





## Sensitivity analysis

It has also been investigated which settings can be changed to get the error down further. These were motivated by factors which have been analyzed in the [paper](https://www.sciencedirect.com/science/article/pii/S0273117723008050).
These factors are: 

- ionospheric refraction, as influenced by the min. elevation angle. 
- insufficient dynamic model lacking for instance Coriolis and centrifugal acceleration
- antenna location

The sensitivity analysis has been carried out in the [sensitivity analysis folder](https://github.com/niklasknoell/Microsat-gps-sim/tree/Bas/trajectory_generation/sensitivity%20analysis). To enable automation, a user only has to choose a [name of the sensitivity simulation](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/sensitivity%20analysis/choose_simulation.py) of interest and run the [run simulation file](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/sensitivity%20analysis/run_simulation.py), which will run all code in the right order. 


The ionospheric refraction has been tested on two aspects:

- the minimum required elevation angle
- whether or not the RF ionospheric corrections are applied on the generated file

Three additional simulations have been tested. One has been tested without the RF ionospheric correction for an elevation angle of 15°. The 0° has already been tested above, which is the default elevation angle.
The other two simulations have been tested with the RF ionospheric correction for an elevation angle of 0° and 15°. 

For the simulation without the RF ionospheric correction, at an elevation angle of 15°, the following figure was obtained:

![image](https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/fe3693cd-074e-4fe9-b10d-bfbd09a01e5f)


By comparing the elevation angle of 15° with the elevation angle of 0° in the previous section, the position error is a couple of meter worse. However, a longer simulation would allow for stronger evidence. It might be that the trade-off between the number of satellites in view vs the quality is better for another angle.
It should be tested for more elevation angles and for a longer duration to come to a more conclusive recommendation. 

For the simulations with the RF ionospheric correction, the following figure was obtained:

<table>
  <tr>
    <td>
      <figure>
        <img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/822832aa-d3cd-4741-9b72-ea3304af33e5" alt="Image 1">
        <figcaption>elevation angle of 0°</figcaption>
      </figure>
    </td>
    <td>
      <figure>
        <img src="https://github.com/niklasknoell/Microsat-gps-sim/assets/74927648/710a4e39-67c2-402a-a7a9-4010adb46128" alt="Image 2">
        <figcaption>elevation angle of 15°</figcaption>
      </figure>
    </td>
  </tr>
</table>


Comparing the above figure with the previous one, it can be seen that the RF ionospheric correction has made the error larger, for both elevation angles, to an unacceptable level. For orbits in LEO, a user is therefore advised to not implement the RF ionospheric correction, but only increase the minimum required elevation angle up to a certain value to obtain a lower error. 


The second factor of the paper, a possibly insufficient dynamic model, has not been tested as the dynamic model of the GNSS could not be (easily) altered. Regardless, it has been hypothesized in the previous section that the Coriolis acceleration is neglected in the dynamic model. In order to also hypothesize whether or not the centrifugal acceleration has been neglected in the dynamic model, a GEO satellite (GOES) which has an equatorial orbit has been run. From literature, neglecting the centrifugal acceleration should result in a constant offset in the radial component. However, it was found that no lock could be obtained for the GOES satellite. Therefore, it could not be hypothesized whether the centrifugal acceleration has been neglected or not. It is hypothesized that the gps-sdr-sim does not work (well) for orbit determination of GEO orbits which have a higher altitude than GNSS satellites.  


Moreover, the influence of the antenna location could not be tested, because while the receiver is orbiting on a virtual trajectory, it is not attached to an actual satellite, and is not obstructed by its satellite body. 

Apart from the three main errors analyzed in the paper, more errors could be investigated. Due to the large number of simulations which have been run to attempt to completely fix the loss of lock in the binary parser, these have not been analyzed. However, the following errors are recommended for further investigation based on the implementation in this repository:

- transmitter and receiver clock offset
- relativistic effect caused by the eccentricity of the GNSS orbits
- light time correction 

These factors are motivated by the course Satellite Orbit Determination (AE4872), given at the Delft University of Technology. In order to analyze any error of interest, a user has to:

- Modify the settings accordingly such that the error of interest can be analyzed 
- Generate a .txt as returned by the binary parser and put it in the [file folder](https://github.com/niklasknoell/Microsat-gps-sim/tree/Bas/trajectory_generation/sensitivity%20analysis/Files)
- Give a desired name in the [choose simulation file](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/sensitivity%20analysis/choose_simulation.py)
- Run the [run simulation file](https://github.com/niklasknoell/Microsat-gps-sim/blob/Bas/trajectory_generation/sensitivity%20analysis/run_simulation.py) 
- The generated results can then be viewed in the [figures folder](https://github.com/niklasknoell/Microsat-gps-sim/tree/Bas/trajectory_generation/sensitivity%20analysis/Figures) and compared with the baseline error

  
  







