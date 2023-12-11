# Load standard modules
import numpy as np

import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
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



#---------------------------Plotting---------------------------#
dpi = 300

states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
print(states)

# xyz = states[:,1:4]
# VxVyVz = states[:,4:7]
#
#
# RSW_list = []
# TNW_list = []
#
# for i in range(np.shape(xyz)[0]):
#
#     rotation_rsw_to_inertial = frame_conversion.rsw_to_inertial_rotation_matrix(states[i,1:])
#
#     pos = np.matmul(np.linalg.inv(rotation_rsw_to_inertial),xyz[i,:])
#     vel = np.matmul(np.linalg.inv(rotation_rsw_to_inertial),VxVyVz[i,:])
#     RSW = np.concatenate((pos,vel))
#
#     RSW_list.append(RSW)
#
#
#     rotation_tnw_to_inertial = frame_conversion.tnw_to_inertial_rotation_matrix(states[i,1:])
#
#     pos = np.matmul(np.linalg.inv(rotation_tnw_to_inertial),xyz[i,:])
#     vel = np.matmul(np.linalg.inv(rotation_tnw_to_inertial),VxVyVz[i,:])
#     TNW = np.concatenate((pos,vel))
#
#     TNW_list.append(TNW)
#
#
#
#
#
#
#
# RSW = np.array(RSW_list)
# TNW = np.array(TNW_list)



dep_vars = np.genfromtxt(os.path.join(file_path,"dep_vars.txt").replace("\\.", "."), delimiter=',')
time = dep_vars[:,0]
longitude = dep_vars[:,1]
latitude = dep_vars[:,2]
altitude = dep_vars[:,3]



# convert to degrees
longitude = np.rad2deg(longitude)
latitude = np.rad2deg(latitude)


fig, ax = plt.subplots()
ax.set_title("ground track of Delfi-PQ")
ax.scatter(longitude, latitude, s=1)
ax.set_xlabel('Longitude [deg]')
ax.set_ylabel('Latitude [deg]')
ax.grid()
ax.set_xlim([min(longitude), max(longitude)])
ax.set_yticks(np.arange(-90, 91, step=45))

output_path = os.path.join(figures_path,"lon_lat.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


fig, ax = plt.subplots()
ax.set_title("altitude over time of Delfi-PQ")
ax.scatter(time, altitude, s=1)
ax.set_xlabel('time [s]')
ax.set_ylabel('altitude [m]')
ax.grid()

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


print("end")
plt.show()