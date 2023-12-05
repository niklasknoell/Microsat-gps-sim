# Load standard modules
import numpy as np

import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.kernel.interface import spice
from tudatpy import numerical_simulation
from tudatpy.kernel.numerical_simulation import environment
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup
from tudatpy.kernel.astro import element_conversion
from tudatpy import constants
from tudatpy.util import result2array
# from tudatpy.kernel.astro.time_conversion import DateTime

from tudatpy.kernel.astro import frame_conversion

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



#-----------------------------------Simulation-----------------------------------#

np.set_printoptions(precision=16)

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

bodies.get("Delfi-PQ").mass = 0.6


# Create aerodynamic coefficient interface settings, and add to vehicle
reference_area = (4*0.18*0.05+2*0.05*0.05)/4  # Average projection area of a 3U CubeSat
drag_coefficient = 1.2
aero_coefficient_settings = environment_setup.aerodynamic_coefficients.constant(
    reference_area, [drag_coefficient, 0, 0]
)
environment_setup.add_aerodynamic_coefficient_interface(
    bodies, "Delfi-PQ", aero_coefficient_settings)


# Create radiation pressure settings, and add to vehicle
reference_area_radiation = (4*0.18*0.05+2*0.05*0.05)/4  # Average projection area of a 3U CubeSat
radiation_pressure_coefficient = 1.2
occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies
)
environment_setup.add_radiation_pressure_interface(
    bodies, "Delfi-PQ", radiation_pressure_settings)


# Define bodies that are propagated
bodies_to_propagate = ["Delfi-PQ"]

# Define central bodies of propagation
central_bodies = ["Earth"]


# Define accelerations acting on Delfi-PQ by Sun and Earth.
accelerations_settings_delfi_PQ = dict(
    Sun=[
        propagation_setup.acceleration.cannonball_radiation_pressure(),
        propagation_setup.acceleration.point_mass_gravity()
    ],
    Earth=[
        propagation_setup.acceleration.spherical_harmonic_gravity(5, 5),
        propagation_setup.acceleration.aerodynamic()
    ],
    Moon=[
        propagation_setup.acceleration.point_mass_gravity()
    ],
    # Mars=[
    #     propagation_setup.acceleration.point_mass_gravity()
    # ],
    # Venus=[
    #     propagation_setup.acceleration.point_mass_gravity()
    # ]
)

# Create global accelerations settings dictionary.
acceleration_settings = {"Delfi-PQ": accelerations_settings_delfi_PQ}

# Create acceleration models.
acceleration_models = propagation_setup.create_acceleration_models(
    bodies,
    acceleration_settings,
    bodies_to_propagate,
    central_bodies)



# Retrieve the initial state of Delfi-PQ using Two-Line-Elements (TLEs)
delfi_tle = environment.Tle(
    "1 51074U 22002CU  23339.18052634  .00274772  00000+0  19782-2 0  9999",
    "2 51074  97.4306  56.6161 0005199 323.2644  36.8262 15.72763456105459"
)
delfi_ephemeris = environment.TleEphemeris( "Earth", "J2000", delfi_tle, False )
initial_state = delfi_ephemeris.cartesian_state( simulation_start_epoch )


# Define list of dependent variables to save
dependent_variables_to_save = [
    propagation_setup.dependent_variable.longitude("Delfi-PQ", "Earth"),
    propagation_setup.dependent_variable.latitude("Delfi-PQ", "Earth"),
    propagation_setup.dependent_variable.altitude("Delfi-PQ", "Earth"),

]


# Create termination settings
termination_condition = propagation_setup.propagator.time_termination(simulation_end_epoch)

# Create numerical integrator settings
fixed_step_size = 10
integrator_settings = propagation_setup.integrator.runge_kutta_4(fixed_step_size)


# Create propagation settings
propagator_settings = propagation_setup.propagator.translational(
    central_bodies,
    acceleration_models,
    bodies_to_propagate,
    initial_state,
    simulation_start_epoch,
    integrator_settings,
    termination_condition,
    output_variables=dependent_variables_to_save
)


# Create simulation object and propagate the dynamics
dynamics_simulator = numerical_simulation.create_dynamics_simulator(
    bodies, propagator_settings
)

# Extract the resulting state and dependent variable history and convert it to an ndarray
states = dynamics_simulator.state_history
states = result2array(states)
dep_vars = dynamics_simulator.dependent_variable_history
dep_vars = result2array(dep_vars)


# Save states as a text file
states_df = pd.DataFrame(states, columns=['time', 'x', 'y', 'z', 'Vx', 'Vy', 'Vz'])
pd.set_option('colheader_justify', 'center')
file_path_states = os.path.join(file_path, "states.txt")
states_df.to_csv(file_path_states, sep='\t', index=False,encoding='ascii',float_format='%.16f')




#---------------------------Plotting---------------------------#

dpi = 300

xyz = states[:,1:4]
VxVyVz = states[:,4:7]


RSW_list = []

for i in range(np.shape(xyz)[0]):

    rotation_rsw_to_inertial = frame_conversion.rsw_to_inertial_rotation_matrix(states[i,1:])

    pos = np.matmul(np.linalg.inv(rotation_rsw_to_inertial),xyz[i,:])
    vel = np.matmul(np.linalg.inv(rotation_rsw_to_inertial),VxVyVz[i,:])
    RSW = np.concatenate((pos,vel))
    print(RSW)
    # print(np.shape(RSW))
    # print(type(RSW))

    RSW_list.append(RSW)

# print(RSW_list)
RSW = np.array(RSW_list)



# Plot ground track for a period of 3 hours
time = dep_vars[:,0]
longitude = dep_vars[:,1]
latitude = dep_vars[:,2]
altitude = dep_vars[:,3]


# convert to degrees
longitude = np.rad2deg(longitude)
latitude = np.rad2deg(latitude)

# save longitude, latitude, altitude to file
combined_array = np.column_stack((time, longitude, latitude, altitude))
df = pd.DataFrame(combined_array, columns=['time','longitude','latitude','altitude'])
pd.set_option('colheader_justify', 'center')
file_path_lla = os.path.join(file_path, "lon_lat_alt.txt")
df.to_csv(file_path_lla, sep='\t', index=False,encoding='ascii',float_format='%.16f')


fig, ax = plt.subplots()
ax.set_title("ground track of Delfi-PQ")
ax.scatter(longitude, latitude, s=1)
ax.set_xlabel('Longitude [deg]')
ax.set_ylabel('Latitude [deg]')
ax.grid()
ax.set_xlim([min(longitude), max(longitude)])
ax.set_yticks(np.arange(-90, 91, step=45))

output_path = os.path.join(figures_path,"lon_lat_alt.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


fig, ax = plt.subplots()
ax.set_title("altitude over time of Delfi-PQ")
ax.scatter(time, altitude, s=1)
ax.set_xlabel('time [s]')
ax.set_ylabel('altitude [m]')
ax.grid()
# ax.set_xlim([min(longitude), max(longitude)])
# ax.set_yticks(np.arange(-90, 91, step=45))

output_path = os.path.join(figures_path,"alt_over_t.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')



fig, ax = plt.subplots()
ax.set_title("RSW position over time of Delfi-PQ")
ax.scatter(time, RSW[:,0], s=1,label="R position")
ax.scatter(time, RSW[:,1], s=1,label="S position")
ax.scatter(time, RSW[:,2], s=1,label="W position")
ax.set_xlabel('time [s]')
ax.set_ylabel('RSW position components [m]')
ax.grid()
ax.legend()

output_path = os.path.join(figures_path,"RSW_position.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')




fig, ax = plt.subplots()
ax.set_title("RSW velocity over time of Delfi-PQ")
ax.scatter(time, RSW[:,3], s=1,label="R velocity")
ax.scatter(time, RSW[:,4], s=1,label="S velocity")
ax.scatter(time, RSW[:,5], s=1,label="W velocity")
ax.set_xlabel('time [s]')
ax.set_ylabel('RSW velocity components [m/s]')
ax.grid()
ax.legend()

output_path = os.path.join(figures_path,"RSW_velocity.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


plt.show()