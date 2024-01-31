import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Load tudatpy modules
from tudatpy.kernel.astro import two_body_dynamics
from tudatpy import constants

from choose_simulation import sim_name, sim_name_file  # import simulation name and file


#-----------------------Directories-----------------------#

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

# Create folder for files if needed
file_path = os.path.join(parent_dir, "sensitivity analysis","Files").replace("\\.", ".")
if os.path.exists(file_path):
    pass
else:
    os.makedirs(file_path)

figures_path = os.path.join(parent_dir, "sensitivity analysis" , "Figures").replace("\\.", ".")
if os.path.exists(figures_path):
    pass
else:
    os.makedirs(figures_path)


#---------------------------Load Kepler elements---------------------------#

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


keplerian_GPS = np.genfromtxt(os.path.join(file_path,sim_name + "keplerian_GPS.txt").replace("\\.", "."), delimiter=',')
initial_time = keplerian_GPS[0,0]
end_simulation = 580
index = np.where(keplerian_GPS[:, 0] >= end_simulation)[0][0]
keplerian_GPS = keplerian_GPS[:index+1, :]


keplerian = np.genfromtxt(os.path.join(file_path,"keplerian.txt").replace("\\.", "."), delimiter=',')
index = np.where(keplerian[:, 0] >= initial_time)[0][0]
keplerian = keplerian[index:,:]
keplerian = keplerian[::10]
index = np.where(keplerian[:, 0] >= end_simulation)[0][0]
keplerian = keplerian[:index, :]
time = keplerian[:,0]


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(9, 12))
fig.suptitle('Evolution of error in Kepler elements')

# Semi-major Axis
x1, y1 = time, keplerian[:,1]
x2, y2 = keplerian_GPS[:,0], keplerian_GPS[:,1]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)

ax1.scatter(x1, (y2_interp -y1) / 1e3)
ax1.set_ylabel('Semi-major axis [km]')

# Eccentricity
x1, y1 = time, keplerian[:,2]
x2, y2 = keplerian_GPS[:,0], keplerian_GPS[:,2]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)

ax2.scatter(time, y2_interp -y1)
ax2.set_ylabel('Eccentricity [-]')

# Inclination
keplerian_GPS[:,3] = np.rad2deg(keplerian_GPS[:,3])
keplerian[:,3] = np.rad2deg(keplerian[:,3])

x1, y1 = time, keplerian[:,3]
x2, y2 = keplerian_GPS[:,0], keplerian_GPS[:,3]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)

ax3.scatter(time, y2_interp -y1)
ax3.set_ylabel('Inclination [deg]')

# Argument of Periapsis
keplerian_GPS[:,4] = np.rad2deg(keplerian_GPS[:,4])
keplerian[:,4] = np.rad2deg(keplerian[:,4])

x1, y1 = time, keplerian[:,4]
x2, y2 = keplerian_GPS[:,0], keplerian_GPS[:,4]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)

# omega_diff[np.where(omega_diff>180)] = omega_diff[np.where(omega_diff>180)] - 360
# omega_diff[np.where(omega_diff<-180)] = omega_diff[np.where(omega_diff<-180)] + 360

ax4.scatter(time, y2_interp -y1)
ax4.set_ylabel('Argument of Periapsis [deg]')

# Right Ascension of the Ascending Node
keplerian_GPS[:,5] = np.rad2deg(keplerian_GPS[:,5])
keplerian[:,5] = np.rad2deg(keplerian[:,5])

x1, y1 = time, keplerian[:,5]
x2, y2 = keplerian_GPS[:,0], keplerian_GPS[:,5]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)

ax5.scatter(time, y2_interp -y1)
ax5.set_ylabel('RAAN [deg]')

# True Anomaly
keplerian_GPS[:,6] = np.rad2deg(keplerian_GPS[:,6])
keplerian[:,6] = np.rad2deg(keplerian[:,6])

x1, y1 = time, keplerian[:,6]
x2, y2 = keplerian_GPS[:,0], keplerian_GPS[:,6]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)

ax6.scatter(time, y2_interp -y1)
ax6.set_ylabel('True Anomaly [deg]')

# ax6.scatter(time,np.rad2deg(keplerian_GPS[:,6]))
# ax6.scatter(time,np.rad2deg(keplerian[:,6]))
# ax6.set_yticks(np.arange(0, 361, step=60))


for ax in fig.get_axes():
    ax.set_xlabel('time [s]')
    ax.set_xlim([min(time), max(time)])
    ax.grid()
plt.tight_layout()


output_path = os.path.join(figures_path,sim_name + "keplerian_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


# plt.show()