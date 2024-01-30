#----------------------------file purely for testing----------------------------#

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

xyz_ECEF_binary = np.genfromtxt(os.path.join(file_path,"binary.txt").replace("\\.", "."), delimiter=',')
xyz_ECEF_binary[:,0] -= 3.2
initial_time = xyz_ECEF_binary[0,0]
end_simulation = 2000
index = np.where(xyz_ECEF_binary[:, 0] >= end_simulation)[0][0]
xyz_ECEF_binary = xyz_ECEF_binary[:index, :]
print(np.shape(xyz_ECEF_binary))


xyz_ECEF = np.genfromtxt(os.path.join(file_path,"xyz_ECEF.txt").replace("\\.", "."), delimiter=',')
index = np.where(xyz_ECEF[:, 0] >= initial_time)[0][0]
xyz_ECEF = xyz_ECEF[index:,:]
xyz_ECEF = xyz_ECEF[::10]
index = np.where(xyz_ECEF[:, 0] >= end_simulation)[0][0]
xyz_ECEF = xyz_ECEF[:index+1, :]
print(np.shape(xyz_ECEF))



fig, ax = plt.subplots()

ax.scatter(xyz_ECEF[:,0], xyz_ECEF[:,3], s=5,label="Benchmark")
ax.scatter(xyz_ECEF_binary[:,0], xyz_ECEF_binary[:,3], s=5,label="GNSS")
ax.plot(xyz_ECEF[:,0],xyz_ECEF_binary[:,3] - xyz_ECEF[:,3])


ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('position component error [m]',fontsize=16)
ax.grid()
ax.tick_params(axis='both', which='major', labelsize=16)
ax.legend(fontsize=20)


plt.show()