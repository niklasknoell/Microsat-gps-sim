# Load standard modules
import numpy as np
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.astro import frame_conversion
from tudatpy.numerical_simulation import estimation_setup
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup
from tudatpy.kernel.interface import spice
from tudatpy.kernel.astro.time_conversion import DateTime
from tudatpy.numerical_simulation import environment
from tudatpy import constants

import pandas as pd
import os
import sys
from scipy.interpolate import interp1d


#-----------------------Directories-----------------------#

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

# Create folder for files if needed
file_path = os.path.join(parent_dir, "Files").replace("\\.", ".")
if os.path.exists(file_path):
    pass
else:
    os.makedirs(file_path)

figures_path = os.path.join(parent_dir, "Figures").replace("\\.", ".")
if os.path.exists(figures_path):
    pass
else:
    os.makedirs(figures_path)

#--------------------------------ECEF to ECI conversion--------------------------------#

# retrieve GPS states in ECEF, which are to be converted to ECI
states_GPS = np.genfromtxt(os.path.join(file_path,"binary_noiono.txt").replace("\\.", "."), delimiter=',')
# states_GPS[:,0] -= 4
initial_time = states_GPS[0,0]
end_simulation = 2000
index = np.where(states_GPS[:, 0] >= end_simulation)[0][0]
states_GPS = states_GPS[:index+1, :]

# retrieve benchmark states already in ECI
states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
index = np.where(states[:, 0] >= initial_time)[0][0]
states = states[index:,:]
states = states[::10]
index = np.where(states[:, 0] >= end_simulation)[0][0]
states = states[:index, :]


# Load spice kernels
spice.load_standard_kernels()

# get time, one JULIAN day is 86400.0 seconds
years = 23
days = 339
hours = 8
minutes = 10
seconds = 36

orbital_period = 91.6*60


# Set simulation start and end epochs, corresponding to the TLE obtain from e.g. Celestrak
simulation_start_epoch = years * constants.JULIAN_YEAR + days * constants.JULIAN_DAY + hours*3600 + minutes*60 + seconds
simulation_end_epoch = simulation_start_epoch + 2*orbital_period


# Define string names for bodies to be created from default.
bodies_to_create = ["Earth"]

# Use "Earth"/"J2000" as global frame origin and orientation.
global_frame_origin = "Earth"
global_frame_orientation = "J2000"

# Create default body settings, usually from `spice`.
body_settings = environment_setup.get_default_body_settings(
    bodies_to_create,
    global_frame_origin,
    global_frame_orientation)


# Create system of selected celestial bodies
bodies = environment_setup.create_system_of_bodies(body_settings)

earth_rotation_model = bodies.get("Earth").rotation_model


states_GPS_ECI = []

for t in range(np.shape(states_GPS)[0]):

    sim_time = states_GPS[t,0]
    R = environment.RotationalEphemeris.body_fixed_to_inertial_rotation(earth_rotation_model,
                                                                        simulation_start_epoch + sim_time)
    inertial_state_xyz = np.matmul(R, states_GPS[t, 1:4])
    inertial_state_VxVyVz = np.matmul(R, states_GPS[t, 4:])
    inertial_state = np.concatenate([inertial_state_xyz, inertial_state_VxVyVz])
    inertial_state = np.concatenate([sim_time.reshape(1), inertial_state])

    # inertial_state = environment.transform_to_inertial_orientation(
    #     states_GPS[t,1:], simulation_start_epoch + sim_time, earth_rotation_model)
    states_GPS_ECI.append(inertial_state)

states_GPS_ECI = np.array(states_GPS_ECI)


# Save the ECI for other conversions
df = pd.DataFrame(states_GPS_ECI, columns=['time', 'x', 'y', 'z', 'Vx', 'Vy', 'Vz'])
pd.set_option('colheader_justify', 'center')
file_path_states = os.path.join(file_path, "states_ECI_GPS.txt")
df.to_csv(file_path_states, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')


#-----------------plotting in this file just for verification-----------------#
fig, ax = plt.subplots()
# ax.set_title("position components error over time")

ax.scatter(states[:,0], states[:,1], s=5,label="Benchmark")
# ax.scatter(states[:,0], states[:,2], s=5,label="Benchmark")
# ax.scatter(states[:,0], states[:,3], s=5,label="Benchmark")


ax.scatter(states_GPS_ECI[:,0], states_GPS_ECI[:,1], s=5,label="GNSS")
# # ax.scatter(states_GPS[:,0], states_GPS_ECI[:,2], s=5,label="GNSS")
# # ax.scatter(states_GPS[:,0], states_GPS_ECI[:,3], s=5,label="GNSS")

#------------------------------necessary interpolation------------------------------#
x1, y1 = states[:, 0], states[:, 1]
x2, y2 = states_GPS_ECI[:, 0], states_GPS_ECI[:, 1]

interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)


plt.plot(x1,y2_interp -y1)


ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('position component error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)


plt.show()