# Load standard modules
import numpy as np

import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.kernel.interface import spice
from tudatpy import numerical_simulation
from tudatpy.kernel.numerical_simulation import environment
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup
from tudatpy.util import result2array
from tudatpy.kernel.astro.time_conversion import DateTime


import pandas as pd
import os

#-----------------------Directories-----------------------#

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

# Create folder for files if needed
file_path = os.path.join(parent_dir, "Astrocast Files").replace("\\.", ".")
if os.path.exists(file_path):
    pass
else:
    os.makedirs(file_path)



#-----------------------------------Simulation-----------------------------------#

np.set_printoptions(precision=16)

# Load spice kernels
spice.load_standard_kernels()

# get time, one JULIAN day is 86400.0 seconds
years = 2024
months = 1
days = 23
hours = 17
minutes = 52
seconds = 37


simulation_start_epoch = DateTime(years, months, days, hours,minutes,seconds).epoch()
simulation_end_epoch = simulation_start_epoch + 360.0


# Define string names for bodies to be created from default.
bodies_to_create = ["Sun", "Earth", "Moon"]

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
bodies.create_empty_body("Astrocast Cubesat")

bodies.get("Astrocast Cubesat").mass = 5


# Create aerodynamic coefficient interface settings, and add to vehicle
reference_area = (4*0.37*0.1+2*0.1*0.1)/4  # Average projection area of a 3U CubeSat
drag_coefficient = 1.2
aero_coefficient_settings = environment_setup.aerodynamic_coefficients.constant(
    reference_area, [drag_coefficient, 0, 0]
)
environment_setup.add_aerodynamic_coefficient_interface(
    bodies, "Astrocast Cubesat", aero_coefficient_settings)


# Create radiation pressure settings, and add to vehicle
reference_area_radiation = (4*0.37*0.1+2*0.1*0.1)/4  # Average projection area of a 3U CubeSat
radiation_pressure_coefficient = 1.2
occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies
)
environment_setup.add_radiation_pressure_interface(
    bodies, "Astrocast Cubesat", radiation_pressure_settings)


# Define bodies that are propagated
bodies_to_propagate = ["Astrocast Cubesat"]

# Define central bodies of propagation
central_bodies = ["Earth"]


# Define accelerations acting on Delfi-PQ by Sun and Earth.
accelerations_settings_astrocast = dict(
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
    ]
)

# Create global accelerations settings dictionary.
acceleration_settings = {"Astrocast Cubesat": accelerations_settings_astrocast}

# Create acceleration models.
acceleration_models = propagation_setup.create_acceleration_models(
    bodies,
    acceleration_settings,
    bodies_to_propagate,
    central_bodies)



# Retrieve the initial state of Delfi-PQ using Two-Line-Elements (TLEs)
tle = environment.Tle(
    "1 51074U 22002CU  23339.18052634  .00274772  00000+0  19782-2 0  9999",
    "2 51074  97.4306  56.6161 0005199 323.2644  36.8262 15.72763456105459"
)
ephemeris = environment.TleEphemeris( "Earth", "J2000", tle, False )
initial_state = ephemeris.cartesian_state( simulation_start_epoch )


# Define list of dependent variables to save
dependent_variables_to_save = [
    propagation_setup.dependent_variable.longitude("Astrocast Cubesat", "Earth"),
    propagation_setup.dependent_variable.latitude("Astrocast Cubesat", "Earth"),
    propagation_setup.dependent_variable.altitude("Astrocast Cubesat", "Earth"),
    propagation_setup.dependent_variable.central_body_fixed_cartesian_position("Astrocast Cubesat","Earth"),
    propagation_setup.dependent_variable.body_fixed_groundspeed_velocity("Astrocast Cubesat","Earth"),
    propagation_setup.dependent_variable.keplerian_state("Astrocast Cubesat", "Earth")
]


# Create termination settings
termination_condition = propagation_setup.propagator.time_termination(simulation_end_epoch)

# Create numerical integrator settings
fixed_step_size = 0.1

integrator_settings = propagation_setup.integrator.runge_kutta_fixed_step(
    time_step = fixed_step_size,
    coefficient_set = propagation_setup.integrator.rkf_89,
    order_to_use = propagation_setup.integrator.higher )



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
states[:, 0] -= simulation_start_epoch  # make time start at 0 sec as required
print(simulation_start_epoch)
print(states)
dep_vars = dynamics_simulator.dependent_variable_history
dep_vars = result2array(dep_vars)
dep_vars[:,1] = np.rad2deg(dep_vars[:,1]) # convert to degrees
dep_vars[:,2] = np.rad2deg(dep_vars[:,2])  # convert to degrees
dep_vars[:, 0] -= simulation_start_epoch  # make time start at 0 sec as required
keplerian = dep_vars[:,10:]
print(dep_vars)


# # Save states as a text file: time,x,y,z,Vx,Vy,Vz
# states_df = pd.DataFrame(states, columns=['time', 'x', 'y', 'z', 'Vx', 'Vy', 'Vz'])
# pd.set_option('colheader_justify', 'center')
# file_path_states = os.path.join(file_path, "states.txt")
# states_df.to_csv(file_path_states, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')
#
# # Save dependent variables as a text file: time,longitude,latitude,altitude
# dep_vars_df = pd.DataFrame(dep_vars)
# file_path_dep_vars = os.path.join(file_path, "dep_vars.txt")
# dep_vars_df.to_csv(file_path_dep_vars, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')
#
# # Save Keplerian elements
# keplerian_df = pd.DataFrame(keplerian)
# file_path_keplerian = os.path.join(file_path, "keplerian.txt")
# keplerian_df.to_csv(file_path_keplerian, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')




# x, y, z coordinates in ECEF
file_path_ECEF = os.path.join(file_path, "xyz_ECEF_short.txt")
data_slice = dep_vars[:, [0, 4, 5, 6]]
df = pd.DataFrame(data_slice)
df.to_csv(file_path_ECEF, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')

# # lat, lon, alt (already ECEF)
# file_path_lla = os.path.join(file_path, "lat_lon_alt.txt")
# data_slice = dep_vars[:, [0, 2, 1, 3]]
# df = pd.DataFrame(data_slice)
# df.to_csv(file_path_lla, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')
