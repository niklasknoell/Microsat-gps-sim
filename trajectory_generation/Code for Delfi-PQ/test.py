#----------------------------This file has been used purely for testing----------------------------#

# Load standard modules
import numpy as np
from matplotlib import pyplot as plt

# Load tudatpy modules
from tudatpy.astro import frame_conversion
from tudatpy.numerical_simulation import estimation_setup
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup
from tudatpy.kernel.interface import spice
from tudatpy.kernel.astro.time_conversion import DateTime
from tudatpy.numerical_simulation import environment
from tudatpy import constants

import pandas as pd
import os
import sys
from scipy.interpolate import interp1d


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



states_GPS = np.genfromtxt(os.path.join(file_path,"binary_noiono_0deg.txt").replace("\\.", "."), delimiter=',')
dep_vars = np.genfromtxt(os.path.join(file_path,"dep_vars.txt").replace("\\.", "."), delimiter=',')
time = dep_vars[:,0]
states = dep_vars[:,4:10]
states = np.concatenate((time.reshape(-1, 1), states), axis=1)


fig, ax = plt.subplots()

ax.scatter(states[:,0],states[:,6])
ax.scatter(states_GPS[:,0],states_GPS[:,6])

ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('position component error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)


plt.show()