#----------------------------file purely for testing----------------------------#

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
from tudatpy.kernel.astro.time_conversion import DateTime

from tudatpy.kernel.astro import frame_conversion

import pandas as pd
import os

#-----------------------Directories-----------------------#

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

# Create folder for files if needed
file_path = os.path.join(parent_dir, "Astrocast").replace("\\.", ".")
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
years = 2024
months = 1
days = 21
hours = 23
minutes = 33
seconds = 35


# DateTime(year=2024,month=1,day=21,hour=23,minute=33,seconds=35)
orbital_period = 95*60

# Set simulation start and end epochs, corresponding to the TLE obtain from e.g. Celestrak
simulation_start_epoch = DateTime(years, months, days, hours,minutes,seconds).epoch()
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
    "1 43798U 18099AS  24021.70115283  .00014813  00000-0  98015-3 0  9997",
    "2 43798  97.5592  87.1577 0012401  79.5466 280.7158 15.07383665280634"
)
delfi_ephemeris = environment.TleEphemeris( "Earth", "J2000", delfi_tle, False )
initial_state = delfi_ephemeris.cartesian_state( simulation_start_epoch )
print(initial_state)


# Define list of dependent variables to save
dependent_variables_to_save = [
    propagation_setup.dependent_variable.longitude("Delfi-PQ", "Earth"),
    propagation_setup.dependent_variable.latitude("Delfi-PQ", "Earth"),
    propagation_setup.dependent_variable.altitude("Delfi-PQ", "Earth"),
    propagation_setup.dependent_variable.central_body_fixed_cartesian_position("Delfi-PQ","Earth"),
    propagation_setup.dependent_variable.body_fixed_groundspeed_velocity("Delfi-PQ","Earth"),
    propagation_setup.dependent_variable.keplerian_state("Delfi-PQ", "Earth")
]


# Create termination settings
termination_condition = propagation_setup.propagator.time_termination(simulation_end_epoch)

# Create numerical integrator settings
fixed_step_size = 0.1
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
states[:, 0] -= simulation_start_epoch  # make time start at 0 sec as required
dep_vars = dynamics_simulator.dependent_variable_history
dep_vars = result2array(dep_vars)
dep_vars[:,1] = np.rad2deg(dep_vars[:,1]) # convert to degrees
dep_vars[:,2] = np.rad2deg(dep_vars[:,2])  # convert to degrees
dep_vars[:, 0] -= simulation_start_epoch  # make time start at 0 sec as required
keplerian = dep_vars[:,10:]

