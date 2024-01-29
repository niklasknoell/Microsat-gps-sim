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


#-----------------------------------Simulation-----------------------------------#

np.set_printoptions(precision=16)

# Load spice kernels
spice.load_standard_kernels()

# get time, one JULIAN day is 86400.0 seconds
years = 2023
months = 12
days = 6
hours = 8
minutes = 10
seconds = 36


simulation_start_epoch = DateTime(years, months, days, hours,minutes,seconds).epoch()
simulation_end_epoch = simulation_start_epoch + 360.0



# Define string names for bodies to be created from default.
bodies_to_create = ["Sun", "Earth", "Moon",]

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
    ]
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
    termination_condition
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
