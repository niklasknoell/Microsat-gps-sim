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


#---------------------------Calculate RSW error---------------------------#

states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
states_GPS = np.genfromtxt(os.path.join(file_path,"states_GPS.txt").replace("\\.", "."), delimiter=',')

xyz = states[:, 1:4]
VxVyVz = states[:, 4:7]

xyz_GPS = states_GPS[:, 1:4]
VxVyVz_GPS = states_GPS[:, 4:7]


RSW_error = []
TNW_error = []

for i in range(np.shape(xyz)[0]):

    rotation_rsw_to_inertial = frame_conversion.rsw_to_inertial_rotation_matrix(states[i, 1:])

    pos = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), xyz[i, :])
    vel = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), VxVyVz[i, :])
    RSW = np.concatenate((pos, vel))

    pos_GPS = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), xyz_GPS[i, :])
    vel_GPS = np.matmul(np.linalg.inv(rotation_rsw_to_inertial), VxVyVz_GPS[i, :])
    RSW_GPS = np.concatenate((pos_GPS, vel_GPS))


    RSW_error.append(RSW-RSW_GPS)


    # rotation_tnw_to_inertial = frame_conversion.tnw_to_inertial_rotation_matrix(states[i, 1:])
    #
    # rotation_inertial_to_tnw = frame_conversion.inertial_to_tnw_rotation_matrix(states[i, 1:])
    # pos = np.matmul(rotation_inertial_to_tnw, xyz[i, :])
    # vel = np.matmul(rotation_inertial_to_tnw, VxVyVz[i, :])
    #
    #
    # # pos = np.matmul(np.linalg.inv(rotation_tnw_to_inertial), xyz[i, :])
    # # vel = np.matmul(np.linalg.inv(rotation_tnw_to_inertial), VxVyVz[i, :])
    # TNW = np.concatenate((pos, vel))
    #
    # TNW_list.append(TNW)

RSW_error= np.array(RSW_error)
print(RSW_error)


RSW_error_df = pd.DataFrame(RSW_error)
file_path_RSW_error = os.path.join(file_path, "RSW_error.txt")
RSW_error_df.to_csv(file_path_RSW_error, sep=',', index=False,header=False,encoding='ascii',float_format='%.16f')



# TNW = np.array(TNW_list)