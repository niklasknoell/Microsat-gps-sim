# Load standard modules
import numpy as np

import matplotlib
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.kernel.astro import frame_conversion

import pandas as pd
import os
from scipy.interpolate import interp1d
import sys

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


#---------------------------Calculate RSW error---------------------------#

# retrieve GPS states in ECI
states_GPS = np.genfromtxt(os.path.join(file_path,"states_ECI_GPS.txt").replace("\\.", "."), delimiter=',')
initial_time = states_GPS[0,0]
end_simulation = 2400
index = np.where(states_GPS[:, 0] >= end_simulation)[0][0]
states_GPS = states_GPS[:index+1, :]

# retrieve benchmark states in ECI
states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
index = np.where(states[:, 0] >= initial_time)[0][0]
states = states[index:,:]
states = states[::10]
index = np.where(states[:, 0] >= end_simulation)[0][0]
states = states[:index, :]


xyz = states[:, 1:4]
VxVyVz = states[:, 4:7]

xyz_GPS = states_GPS[:, 1:4]
VxVyVz_GPS = states_GPS[:, 4:7]

#------------------------------necessary interpolation------------------------------#

x1, y1 = states[:, 0], states[:, 1]
x2, y2 = states_GPS[:, 0], states_GPS[:, 1]
interp_func = interp1d(x2,y2)
x = interp_func(x1)

x1, y1 = states[:, 0], states[:, 2]
x2, y2 = states_GPS[:, 0], states_GPS[:, 2]
interp_func = interp1d(x2,y2)
y = interp_func(x1)

x1, y1 = states[:, 0], states[:, 3]
x2, y2 = states_GPS[:, 0], states_GPS[:, 3]
interp_func = interp1d(x2,y2)
z = interp_func(x1)

xyz_GPS = np.column_stack((x, y, z))


x1, y1 = states[:, 0], states[:, 4]
x2, y2 = states_GPS[:, 0], states_GPS[:, 4]
interp_func = interp1d(x2,y2)
Vx = interp_func(x1)

x1, y1 = states[:, 0], states[:, 5]
x2, y2 = states_GPS[:, 0], states_GPS[:, 5]
interp_func = interp1d(x2,y2)
Vy = interp_func(x1)

x1, y1 = states[:, 0], states[:, 6]
x2, y2 = states_GPS[:, 0], states_GPS[:, 6]
interp_func = interp1d(x2,y2)
Vz = interp_func(x1)

VxVyVz_GPS = np.column_stack((Vx, Vy, Vz))


#------------------------------transformation------------------------------#

RSW_error = []

for i in range(np.shape(xyz)[0]):

    rotation_rsw_to_inertial = frame_conversion.rsw_to_inertial_rotation_matrix(states[i, 1:])

    pos = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), xyz[i, :])
    vel = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), VxVyVz[i, :])
    RSW = np.concatenate((pos, vel))

    pos_GPS = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), xyz_GPS[i, :])
    vel_GPS = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), VxVyVz_GPS[i, :])
    RSW_GPS = np.concatenate((pos_GPS, vel_GPS))


    RSW_error.append(RSW-RSW_GPS)


RSW_error= np.array(RSW_error)


RSW_error_df = pd.DataFrame(RSW_error)
file_path_RSW_error = os.path.join(file_path, "RSW_error.txt")
RSW_error_df.to_csv(file_path_RSW_error, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')


