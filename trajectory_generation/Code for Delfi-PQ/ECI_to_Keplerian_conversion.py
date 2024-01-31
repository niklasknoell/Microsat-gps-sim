# Load standard modules
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.astro import element_conversion
from tudatpy.numerical_simulation import estimation_setup
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup
from tudatpy.kernel.interface import spice
from tudatpy.kernel.astro.time_conversion import DateTime
from tudatpy.numerical_simulation import environment
from tudatpy import constants


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

#--------------------------------ECI to Keplerian conversion--------------------------------#

# Load spice kernels
spice.load_standard_kernels()


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

gravitational_parameter = bodies.get("Earth").gravity_field_model.gravitational_parameter


# retrieve GPS states in ECEF, which are to be converted to ECI
states_GPS = np.genfromtxt(os.path.join(file_path,"states_ECI_GPS.txt").replace("\\.", "."), delimiter=',')
initial_time = states_GPS[0,0]
end_simulation = 2400
index = np.where(states_GPS[:, 0] >= end_simulation)[0][0]
states_GPS = states_GPS[:index+1, :]


keplerian_GPS = []

for t in range(np.shape(states_GPS)[0]):

    sim_time = states_GPS[t, 0]

    keplerian = element_conversion.cartesian_to_keplerian(states_GPS[t, 1:],gravitational_parameter)

    keplerian = np.concatenate([sim_time.reshape(1), keplerian])

    keplerian_GPS.append(keplerian)


keplerian_GPS = np.array(keplerian_GPS)

# Save the ECI for other conversions
df = pd.DataFrame(keplerian_GPS)
pd.set_option('colheader_justify', 'center')
file_path_states = os.path.join(file_path, "keplerian_GPS.txt")
df.to_csv(file_path_states, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')

#-----------------plotting in this file just for verification-----------------#

time = states_GPS[:,0]

fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(9, 12))
fig.suptitle('Evolution of error in Kepler elements')

# Semi-major Axis
ax1.plot(time, (keplerian_GPS[:,1] / 1e3))
ax1.set_ylabel('Semi-major axis [km]')

# Eccentricity
ax2.plot(time, keplerian_GPS[:,2])
ax2.set_ylabel('Eccentricity [-]')

# Inclination
ax3.plot(time, np.rad2deg(keplerian_GPS[:,3]))
ax3.set_ylabel('Inclination [deg]')

# Argument of Periapsis
omega_diff = np.rad2deg(keplerian_GPS[:,4])
# omega_diff[np.where(omega_diff>180)] = omega_diff[np.where(omega_diff>180)] - 360
# omega_diff[np.where(omega_diff<-180)] = omega_diff[np.where(omega_diff<-180)] + 360

ax4.plot(time, omega_diff)
ax4.set_ylabel('Argument of Periapsis [deg]')

# Right Ascension of the Ascending Node
ax5.plot(time, np.rad2deg(keplerian_GPS[:,5]))
ax5.set_ylabel('RAAN [deg]')

# True Anomaly
true_anomaly_diff = np.rad2deg(keplerian_GPS[:,6])
# omega_diff[np.where(omega_diff>180)] = omega_diff[np.where(omega_diff>180)] - 360
# true_anomaly_diff[np.where(true_anomaly_diff>180)] = true_anomaly_diff[np.where(true_anomaly_diff>180)] - 180

ax6.scatter(time, true_anomaly_diff, s=1)
ax6.set_ylabel('True Anomaly [deg]')
# ax6.set_yticks(np.arange(0, 361, step=60))

for ax in fig.get_axes():
    ax.set_xlabel('time [s]')
    ax.set_xlim([min(time), max(time)])
    ax.grid()
plt.tight_layout()

# plt.show()