# Load standard modules
import sys
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.kernel.astro import frame_conversion

import pandas as pd
import os
from scipy.interpolate import interp1d

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


#---------------------State error---------------------#

# retrieve GPS states in ECI
states_GPS = np.genfromtxt(os.path.join(file_path,sim_name + "states_ECI_GPS.txt").replace("\\.", "."), delimiter=',')
initial_time = states_GPS[0,0]
end_simulation = 800
index = np.where(states_GPS[:, 0] >= end_simulation)[0][0]
states_GPS = states_GPS[:index+1, :]

# retrieve benchmark states in ECI
states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
index = np.where(states[:, 0] >= initial_time)[0][0]
states = states[index:,:]
states = states[::10]
index = np.where(states[:, 0] >= end_simulation)[0][0]
states = states[:index, :]



fig, ax = plt.subplots()
# ax.set_title("position components error over time")

x1, y1 = states[:, 0], states[:, 1]
x2, y2 = states_GPS[:, 0], states_GPS[:, 1]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
ax.scatter(x1,y2_interp -y1,label='$\Delta$x')

x1, y1 = states[:, 0], states[:, 2]
x2, y2 = states_GPS[:, 0], states_GPS[:, 2]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
ax.scatter(x1,y2_interp -y1,label='$\Delta$y')

x1, y1 = states[:, 0], states[:, 3]
x2, y2 = states_GPS[:, 0], states_GPS[:, 3]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
ax.scatter(x1,y2_interp -y1,label='$\Delta$z')


ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('position component error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)

output_path = os.path.join(figures_path,sim_name + "states_position_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')



fig, ax = plt.subplots()
# ax.set_title("velocity components error over time")

x1, y1 = states[:, 0], states[:, 4]
x2, y2 = states_GPS[:, 0], states_GPS[:, 4]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
ax.scatter(x1,y2_interp -y1,label='$\Delta V_{x}$')

x1, y1 = states[:, 0], states[:, 5]
x2, y2 = states_GPS[:, 0], states_GPS[:, 5]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
ax.scatter(x1,y2_interp -y1,label='$\Delta V_{y}$')

x1, y1 = states[:, 0], states[:, 6]
x2, y2 = states_GPS[:, 0], states_GPS[:, 6]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
ax.scatter(x1,y2_interp -y1,label='$\Delta V_{z}$')


ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('velocity component error [m/s]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)
ax.set_ylim([-0.15, 0.15])

output_path = os.path.join(figures_path,sim_name + "states_velocity_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')



#---------------------RMSE and 3D position and velocity error---------------------#

RMSE = np.genfromtxt(os.path.join(file_path,sim_name + "RMSE_position.txt").replace("\\.", "."), delimiter=',')
pos_error = np.genfromtxt(os.path.join(file_path,sim_name + "position_error.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], RMSE, s=1,label="RMSE of position")
ax.scatter(states[:,0], pos_error, s=1,label="position error")
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)

output_path = os.path.join(figures_path,sim_name + "RMSE_position.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


RMSE = np.genfromtxt(os.path.join(file_path,sim_name + "RMSE_velocity.txt").replace("\\.", "."), delimiter=',')
vel_error = np.genfromtxt(os.path.join(file_path,sim_name + "velocity_error.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()
# ax.set_title("velocity components error over time")
ax.scatter(states[:,0], RMSE, s=1,label="RMSE of velocity")
ax.scatter(states[:,0], vel_error, s=1,label="velocity error")
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('error [m/s]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)
ax.set_ylim([10**(-2), 10**(1)])
ax.set_yscale('log')

output_path = os.path.join(figures_path,sim_name + "RMSE_velocity.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')

#---------------------RSW error---------------------#

RSW_error = np.genfromtxt(os.path.join(file_path,sim_name + "RSW_error.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], RSW_error[:,0], s=5,label='R')
# ax.plot(states[:,0], RSW_error[:,0],label='R')
ax.scatter(states[:,0], RSW_error[:,1], s=5,label='S')
# ax.plot(states[:,0], RSW_error[:,1],label='S')
ax.scatter(states[:,0], RSW_error[:,2], s=5,label='W')
# ax.plot(states[:,0], RSW_error[:,2],label='W')
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('Error in R, S, W direction [m]',fontsize=16)
ax.grid()
ax.legend(fontsize=20)

output_path = os.path.join(figures_path,sim_name + "RSW_position_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], RSW_error[:,3], s=5,label='R')
# ax.plot(states[:,0], RSW_error[:,3],label='R')
ax.scatter(states[:,0], RSW_error[:,4], s=5,label='S')
# ax.plot(states[:,0], RSW_error[:,4],label='S')
ax.scatter(states[:,0], RSW_error[:,5], s=5,label='W')
# ax.plot(states[:,0], RSW_error[:,5],label='W')
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('Error in R, S, W direction [m/s]',fontsize=16)
ax.grid()
ax.legend(fontsize=20)

output_path = os.path.join(figures_path,sim_name + "RSW_velocity_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')



plt.show()