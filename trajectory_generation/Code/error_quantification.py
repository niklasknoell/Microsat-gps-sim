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



#---------------------State error---------------------#

states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
states_GPS = np.genfromtxt(os.path.join(file_path,"states_GPS.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], states_GPS[:,1]-states[:,1], s=5)
ax.plot(states[:,0], states_GPS[:,1]-states[:,1],label='$\Delta$x')
ax.scatter(states[:,0], states_GPS[:,2]-states[:,2], s=5)
ax.plot(states[:,0], states_GPS[:,2]-states[:,2],label='$\Delta$y')
ax.scatter(states[:,0], states_GPS[:,3]-states[:,3], s=5)
ax.plot(states[:,0], states_GPS[:,3]-states[:,3],label='$\Delta$z')
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('position component error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)

output_path = os.path.join(figures_path,"states_position_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], states_GPS[:,4]-states[:,4], s=5)
ax.plot(states[:,0], states_GPS[:,4]-states[:,4],label='$\Delta V_{x}$')
ax.scatter(states[:,0], states_GPS[:,5]-states[:,5], s=5)
ax.plot(states[:,0], states_GPS[:,5]-states[:,5],label='$\Delta V_{y}$')
ax.scatter(states[:,0], states_GPS[:,6]-states[:,6], s=5)
ax.plot(states[:,0], states_GPS[:,6]-states[:,6],label='$\Delta V_{z}$')
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('velocity component error [m/s]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)

output_path = os.path.join(figures_path,"states_velocity_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


#---------------------RMSE error---------------------#

RMSE = np.genfromtxt(os.path.join(file_path,"RMSE_position.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], RMSE, s=1)
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('RMSE [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)

output_path = os.path.join(figures_path,"RMSE_position.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


RMSE = np.genfromtxt(os.path.join(file_path,"RMSE_velocity.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], RMSE, s=1)
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('RMSE [m/s]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)

output_path = os.path.join(figures_path,"RMSE_velocity.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')



#---------------------RSW error---------------------#

RSW_error = np.genfromtxt(os.path.join(file_path,"RSW_error.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], RSW_error[:,0], s=5)
ax.plot(states[:,0], RSW_error[:,0],label='R')
ax.scatter(states[:,0], RSW_error[:,1], s=5)
ax.plot(states[:,0], RSW_error[:,1],label='S')
ax.scatter(states[:,0], RSW_error[:,2], s=5)
ax.plot(states[:,0], RSW_error[:,2],label='W')
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('Error in R, S, W direction [m]',fontsize=16)
ax.grid()
ax.legend()


output_path = os.path.join(figures_path,"RSW_position_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


fig, ax = plt.subplots()
# ax.set_title("position components error over time")
ax.scatter(states[:,0], RSW_error[:,3], s=5)
ax.plot(states[:,0], RSW_error[:,3],label='R')
ax.scatter(states[:,0], RSW_error[:,4], s=5)
ax.plot(states[:,0], RSW_error[:,4],label='S')
ax.scatter(states[:,0], RSW_error[:,5], s=5)
ax.plot(states[:,0], RSW_error[:,5],label='W')
ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('Error in R, S, W direction [m/s]',fontsize=16)
ax.grid()
ax.legend()

output_path = os.path.join(figures_path,"RSW_velocity_error.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')



plt.show()