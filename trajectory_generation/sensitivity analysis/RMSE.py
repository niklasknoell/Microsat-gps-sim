# Load standard modules
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import os
from scipy.interpolate import interp1d

from choose_simulation import sim_name, sim_name_file  # import simulation name and file


# -----------------------Directories-----------------------#

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

# ------------------------------Calculate RMSE------------------------------#

# retrieve GPS states in ECI
states_GPS = np.genfromtxt(os.path.join(file_path,sim_name + "states_ECI_GPS.txt").replace("\\.", "."), delimiter=',')
initial_time = states_GPS[0,0]
end_simulation = 600
index = np.where(states_GPS[:, 0] >= end_simulation)[0][0]
states_GPS = states_GPS[:index+1, :]

# retrieve benchmark states in ECI
states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
index = np.where(states[:, 0] >= initial_time)[0][0]
states = states[index:,:]
states = states[::10]
index = np.where(states[:, 0] >= end_simulation)[0][0]
states = states[:index, :]


# -----Position-----#

x1, y1 = states[:, 0], states[:, 1]
x2, y2 = states_GPS[:, 0], states_GPS[:, 1]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
delta_x = y2_interp -y1

x1, y1 = states[:, 0], states[:, 2]
x2, y2 = states_GPS[:, 0], states_GPS[:, 2]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
delta_y = y2_interp -y1

x1, y1 = states[:, 0], states[:, 3]
x2, y2 = states_GPS[:, 0], states_GPS[:, 3]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
delta_z = y2_interp -y1


RMSE_list = []

for t in range(len(delta_x)):
    # print(np.sqrt(np.mean(delta_x[:t]**2 + delta_y[:t]**2 + delta_z[:t]**2)))
    # print()

    RMSE = np.sqrt(np.mean(delta_x[0:t + 1] ** 2 + delta_y[0:t + 1] ** 2 + delta_z[0:t + 1] ** 2))
    RMSE_list.append(RMSE)

RMSE = np.array(RMSE_list)

df = pd.DataFrame(RMSE)
file_path_RMSE = os.path.join(file_path, sim_name + "RMSE_position.txt")
df.to_csv(file_path_RMSE, sep=',', index=False, header=False, encoding='ascii', float_format='%.16f')

# -----velocity-----#

x1, y1 = states[:, 0], states[:, 4]
x2, y2 = states_GPS[:, 0], states_GPS[:, 4]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
delta_x = y2_interp -y1

x1, y1 = states[:, 0], states[:, 5]
x2, y2 = states_GPS[:, 0], states_GPS[:, 5]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
delta_y = y2_interp -y1

x1, y1 = states[:, 0], states[:, 6]
x2, y2 = states_GPS[:, 0], states_GPS[:, 6]
interp_func = interp1d(x2,y2)
y2_interp = interp_func(x1)
delta_z = y2_interp -y1


RMSE_list = []

for t in range(len(delta_x)):
    # print(np.sqrt(np.mean(delta_x[:t]**2 + delta_y[:t]**2 + delta_z[:t]**2)))
    # print()

    RMSE = np.sqrt(np.mean(delta_x[0:t + 1] ** 2 + delta_y[0:t + 1] ** 2 + delta_z[0:t + 1] ** 2))
    RMSE_list.append(RMSE)

RMSE = np.array(RMSE_list)

df = pd.DataFrame(RMSE)
file_path_RMSE = os.path.join(file_path, sim_name + "RMSE_velocity.txt")
df.to_csv(file_path_RMSE, sep=',', index=False, header=False, encoding='ascii', float_format='%.16f')
