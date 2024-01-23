# Load standard modules
import numpy as np

import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.astro import frame_conversion
from tudatpy.numerical_simulation import estimation_setup
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup
from tudatpy.kernel.interface import spice
from tudatpy.kernel.astro.time_conversion import DateTime
from tudatpy.numerical_simulation import environment


import copy
import pandas as pd
import os
import sys

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

states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')

states_GPS = np.genfromtxt(os.path.join(file_path,"states_GPS.txt").replace("\\.", "."), delimiter=',')

xyz_GPS = states_GPS[:, 1:4]
VxVyVz_GPS = states_GPS[:, 4:7]

states_GPS = np.concatenate((xyz_GPS, VxVyVz_GPS), axis=1)

print(states_GPS)


# frame_conversion.body_fixed_to_inertial_rotation_matrix()
# print(estimation_setup.parameter.rotation_pole_position("Earth"))


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
# print(earth_rotation_model)
#
# # Define time at which to determine rotation quantities
# current_time = simulation_start_epoch
#
# # Transform state to inertial frame, using Earth rotation model
# inertial_state = environment.transform_to_inertial_orientation(
#     states_GPS[0,:], current_time, earth_rotation_model )
#
#
# print(states_GPS[0,:])
# print(inertial_state)
# # frame_conversion.body_fixed_to_inertial_rotation_matrix(0,0,0)
# # print(estimation_setup.parameter.rotation_pole_position("Earth").)
#
# print(environment.RotationalEphemeris.body_fixed_to_inertial_rotation(earth_rotation_model,simulation_start_epoch))
#
# print(np.shape(states_GPS))
# print(np.shape(states_GPS)[0])

states_GPS_ECI = []

for t in range(np.shape(states_GPS)[0]):

    sim_time = states_GPS[t,0]

    inertial_state = environment.transform_to_inertial_orientation(
        states_GPS[t,:], simulation_start_epoch + sim_time, earth_rotation_model)
    states_GPS_ECI.append(inertial_state)

states_GPS_ECI = np.array(states_GPS_ECI)
print(states_GPS_ECI)


# fig, ax = plt.subplots()
# # ax.set_title("position components error over time")
# ax.scatter(states[:,0], states[:,1], s=5,label="ECEF")
# ax.scatter(states[:,0], states[:,2], s=5,label="ECEF")
# ax.scatter(states[:,0], states[:,3], s=5,label="ECEF")
# ax.scatter(states_GPS[:,0], states_GPS[:,1], s=5)
# ax.scatter(states_GPS[:,0], states_GPS[:,2], s=5)
# ax.scatter(states_GPS[:,0], states_GPS[:,3], s=5)
# ax.set_xlabel('time [s]',fontsize=16)
# ax.set_ylabel('position component error [m]',fontsize=16)
# ax.grid()
# ax.tick_params(axis='both', which='major', labelsize=16)
# ax.legend(fontsize=20)
#
# plt.show()