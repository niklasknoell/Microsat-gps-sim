import os

import matplotlib
from matplotlib import pyplot as plt
import numpy as np


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


#---------------------------Load Kepler elements---------------------------#
dep_vars = np.genfromtxt(os.path.join(file_path,"dep_vars.txt").replace("\\.", "."), delimiter=',')
time = dep_vars[:,0]

keplerian = np.genfromtxt(os.path.join(file_path,"keplerian.txt").replace("\\.", "."), delimiter=',')
keplerian_GPS = np.genfromtxt(os.path.join(file_path,"keplerian_GPS.txt").replace("\\.", "."), delimiter=',')


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(9, 12))
fig.suptitle('Evolution of error in Kepler elements')

# Semi-major Axis
ax1.plot(time, (keplerian_GPS[:,0]-keplerian[:,0]) / 1e3)
ax1.set_ylabel('Semi-major axis [km]')

# Eccentricity
ax2.plot(time, keplerian_GPS[:,1]-keplerian[:,1])
ax2.set_ylabel('Eccentricity [-]')

# Inclination
ax3.plot(time, np.rad2deg(keplerian_GPS[:,2])-np.rad2deg(keplerian[:,2]))
ax3.set_ylabel('Inclination [deg]')

# Argument of Periapsis
omega_diff = np.rad2deg(keplerian_GPS[:,3])-np.rad2deg(keplerian[:,3])
omega_diff[np.where(omega_diff>180)] = omega_diff[np.where(omega_diff>180)] - 360
omega_diff[np.where(omega_diff<-180)] = omega_diff[np.where(omega_diff<-180)] + 360

ax4.plot(time, omega_diff)
ax4.set_ylabel('Argument of Periapsis [deg]')

# Right Ascension of the Ascending Node
ax5.plot(time, np.rad2deg(keplerian_GPS[:,4])-np.rad2deg(keplerian[:,4]))
ax5.set_ylabel('RAAN [deg]')

# True Anomaly
true_anomaly_diff = np.rad2deg(keplerian_GPS[:,5])-np.rad2deg(keplerian[:,5])

ax6.scatter(time, true_anomaly_diff, s=1)
ax6.set_ylabel('True Anomaly [deg]')
# ax6.set_yticks(np.arange(0, 361, step=60))

for ax in fig.get_axes():
    ax.set_xlabel('time [s]')
    ax.set_xlim([min(time), max(time)])
    ax.grid()
plt.tight_layout()


output_path = os.path.join(figures_path,"keplerian_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')



plt.show()