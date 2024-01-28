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
years = 2024
months = 1
days = 27
hours = 18
minutes = 8
seconds = 5


simulation_start_epoch = DateTime(years, months, days, hours,minutes,seconds).epoch()
simulation_end_epoch = simulation_start_epoch + 1*3600


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
)

# Create global accelerations settings dictionary.
acceleration_settings = {"Delfi-PQ": accelerations_settings_delfi_PQ}

# Create acceleration models.
acceleration_models = propagation_setup.create_acceleration_models(
    bodies,
    acceleration_settings,
    bodies_to_propagate,
    central_bodies)


# Retrieve the initial state of GOES18 using Two-Line-Elements (TLEs)
delfi_tle = environment.Tle(
    "1 51850U 22021A   24027.60098779  .00000101  00000+0  00000+0 0  9997",
    "2 51850   0.0089 296.0219 0000652 324.6271 305.0577  1.00273001  7047"
)
delfi_ephemeris = environment.TleEphemeris( "Earth", "J2000", delfi_tle, False )
initial_state = delfi_ephemeris.cartesian_state( simulation_start_epoch )


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
# integrator_settings = propagation_setup.integrator.runge_kutta_4(fixed_step_size)

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


# x, y, z coordinates in ECEF
file_path_ECEF = os.path.join(file_path, "xyz_ECEF_GOES.txt")
data_slice = dep_vars[:, [0, 4, 5, 6]]
df = pd.DataFrame(data_slice)
df.to_csv(file_path_ECEF, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')



fig, ax = plt.subplots()


ax.scatter(states[:,0], states[:,3], s=5)

ax.set_ylabel('position component error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)





time = dep_vars[:,0]

fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(9, 12))
fig.suptitle('Evolution of error in Kepler elements')

# Semi-major Axis
ax1.plot(time, keplerian[:,0] / 1e3)
ax1.set_ylabel('Semi-major axis [km]')

# Eccentricity
ax2.plot(time, keplerian[:,1])
ax2.set_ylabel('Eccentricity [-]')

# Inclination
ax3.plot(time, np.rad2deg(keplerian[:,2]))
ax3.set_ylabel('Inclination [deg]')

# Argument of Periapsis
omega_diff = np.rad2deg(keplerian[:,3])
# omega_diff[np.where(omega_diff>180)] = omega_diff[np.where(omega_diff>180)] - 360
# omega_diff[np.where(omega_diff<-180)] = omega_diff[np.where(omega_diff<-180)] + 360

ax4.plot(time, omega_diff)
ax4.set_ylabel('Argument of Periapsis [deg]')

# Right Ascension of the Ascending Node
ax5.plot(time, np.rad2deg(keplerian[:,4]))
ax5.set_ylabel('RAAN [deg]')

# True Anomaly
true_anomaly_diff = np.rad2deg(keplerian[:,5])

ax6.scatter(time, true_anomaly_diff, s=1)
ax6.set_ylabel('True Anomaly [deg]')
# ax6.set_yticks(np.arange(0, 361, step=60))

for ax in fig.get_axes():
    ax.set_xlabel('time [s]')
    ax.set_xlim([min(time), max(time)])
    ax.grid()
plt.tight_layout()


plt.show()