# Load standard modules
import numpy as np

import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.kernel.astro import frame_conversion
from tudatpy.kernel.interface import spice
from tudatpy.kernel.astro.time_conversion import DateTime
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup

import pandas as pd
import os

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


#-----------------------Settings-----------------------#

# Load spice kernels
spice.load_standard_kernels()

years = 2023
months = 12
days = 6
hours = 8
minutes = 10
seconds = 36

simulation_start_epoch = DateTime(years, months, days, hours,minutes,seconds).epoch()
simulation_end_epoch = simulation_start_epoch + 360


# Define string names for bodies to be created from default.
bodies_to_create = ["Sun", "Earth", "Moon", "Mars", "Venus"]

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


# Create vehicle objects.
bodies.create_empty_body("Delfi-PQ")



earth_rotation_model = bodies.get("Earth").rotation_model



#---------------------State error---------------------#

# states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
# states = states[0:3601:10, 0:4]
# print(states[-1,:])

states_GPS = np.genfromtxt(os.path.join(file_path,"output_data.txt").replace("\\.", "."), delimiter=',')
initial_time = states_GPS[0,0]
end_simulation = 3200
index = np.where(states_GPS[:, 0] >= end_simulation)[0][0]
states_GPS = states_GPS[:index+1, :]



states = np.genfromtxt(os.path.join(file_path,"xyz_ECEF.txt").replace("\\.", "."), delimiter=',')
index = np.where(states[:, 0] >= initial_time)[0][0]
states = states[index:,:]
states = states[::10]
index = np.where(states[:, 0] >= end_simulation)[0][0]
states = states[:index+1, :]





fig, ax = plt.subplots()
# ax.set_title("position components error over time")

# ax.scatter(states_GPS[:,0], states_GPS[:,1], s=5)
# ax.scatter(states_GPS[:,0], states_GPS[:,2], s=5)
# ax.scatter(states_GPS[:,0], states_GPS[:,3], s=5)

ax.scatter(states_GPS[:,0], states_GPS[:,1], s=20,label="GNSS")
ax.scatter(states[:,0], states[:,1], s=5,label="Benchmark")


ax.plot(states[:,0],states_GPS[:,1]-states[:,1])
# ax.plot(states_GPS[:,0], states_GPS[:,3])
# ax.plot(states[:,0], states[:,3])

# ax.scatter(states_GPS[:,0], states_GPS[:,0], s=20,label="GNSS")
# ax.scatter(states[:,0], states[:,0], s=5,label="Benchmark")


# ax.scatter(states[:,0], states_GPS[:,1]-states[:,1], s=5)
# ax.plot(states[:,0], states_GPS[:,1]-states[:,1],label='$\Delta$x')
# ax.scatter(states[:,0], states_GPS[:,2]-states[:,2], s=5)
# ax.plot(states[:,0], states_GPS[:,2]-states[:,2],label='$\Delta$y')
# ax.scatter(states[:,0], states_GPS[:,3]-states[:,3], s=5)
# ax.plot(states[:,0], states_GPS[:,3]-states[:,3],label='$\Delta$z')
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('position component error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)

plt.show()