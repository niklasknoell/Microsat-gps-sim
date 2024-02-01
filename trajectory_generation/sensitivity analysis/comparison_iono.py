import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


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


#---------------------------compare iono---------------------------#

binary_iono_0deg_states_ECI_GPS = np.genfromtxt(os.path.join(file_path,"binary_iono_0deg_states_ECI_GPS.txt").replace("\\.", "."), delimiter=',')
binary_iono_15deg_states_ECI_GPS = np.genfromtxt(os.path.join(file_path,"binary_iono_15deg_states_ECI_GPS.txt").replace("\\.", "."), delimiter=',')


binary_iono_0deg_position_error = np.genfromtxt(os.path.join(file_path,"binary_iono_0deg_position_error.txt").replace("\\.", "."), delimiter=',')
binary_iono_15deg_position_error = np.genfromtxt(os.path.join(file_path,"binary_iono_15deg_position_error.txt").replace("\\.", "."), delimiter=',')

fig, ax = plt.subplots()

print(np.shape(binary_iono_15deg_states_ECI_GPS[:,0]))
print(np.shape(binary_iono_15deg_position_error))

ax.scatter(binary_iono_15deg_states_ECI_GPS[:,0], binary_iono_15deg_position_error, s=5,label='R')

ax.set_xlabel('time [s]',fontsize=16)
ax.set_ylabel('Error in R, S, W direction [m/s]',fontsize=16)
ax.grid()
ax.legend(fontsize=20)

plt.show()