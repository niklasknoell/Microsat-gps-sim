# Load standard modules
import numpy as np

import matplotlib
from matplotlib import pyplot as plt


# Now you can import tudatpy



import pandas as pd
import os

print(os.environ['PATH'])

# -----------------------Directories-----------------------#

current_dir = os.path.dirname(__file__)
print(current_dir)
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

# ------------------------------Calculate RMSE------------------------------#

# states = np.genfromtxt(os.path.join(file_path, "states.txt").replace("\\.", "."), delimiter=',')
# states_GPS = np.genfromtxt(os.path.join(file_path, "states_GPS.txt").replace("\\.", "."), delimiter=',')

# retrieve GPS states in ECI
states_GPS = np.genfromtxt(os.path.join(file_path,"states_ECI_GPS.txt").replace("\\.", "."), delimiter=',')
initial_time = states_GPS[0,0]
end_simulation = 3200
index = np.where(states_GPS[:, 0] >= end_simulation)[0][0]
states_GPS = states_GPS[:index+1, :]

# retrieve benchmark states in ECI
states = np.genfromtxt(os.path.join(file_path,"states.txt").replace("\\.", "."), delimiter=',')
index = np.where(states[:, 0] >= initial_time)[0][0]
states = states[index:,:]
states = states[::10]
index = np.where(states[:, 0] >= end_simulation)[0][0]
states = states[:index+1, :]


# -----Position-----#
delta_x = states_GPS[:, 1] - states[:, 1]
delta_y = states_GPS[:, 2] - states[:, 2]
delta_z = states_GPS[:, 3] - states[:, 3]
print(delta_x[0:1])
print(delta_y[0:1])
print(delta_z[0:1])

RMSE_list = []

for t in range(len(delta_x)):
    # print(np.sqrt(np.mean(delta_x[:t]**2 + delta_y[:t]**2 + delta_z[:t]**2)))
    # print()

    RMSE = np.sqrt(np.mean(delta_x[0:t + 1] ** 2 + delta_y[0:t + 1] ** 2 + delta_z[0:t + 1] ** 2))
    RMSE_list.append(RMSE)

RMSE = np.array(RMSE_list)
print(RMSE)
print(np.shape(RMSE))
print(np.shape(states))

df = pd.DataFrame(RMSE)
file_path_RMSE = os.path.join(file_path, "RMSE_position.txt")
df.to_csv(file_path_RMSE, sep=',', index=False, header=False, encoding='ascii', float_format='%.16f')

# -----velocity-----#
delta_x = states_GPS[:, 4] - states[:, 4]
delta_y = states_GPS[:, 5] - states[:, 5]
delta_z = states_GPS[:, 6] - states[:, 6]
print(delta_x[0:1])
print(delta_y[0:1])
print(delta_z[0:1])

RMSE_list = []

for t in range(len(delta_x)):
    # print(np.sqrt(np.mean(delta_x[:t]**2 + delta_y[:t]**2 + delta_z[:t]**2)))
    # print()

    RMSE = np.sqrt(np.mean(delta_x[0:t + 1] ** 2 + delta_y[0:t + 1] ** 2 + delta_z[0:t + 1] ** 2))
    RMSE_list.append(RMSE)

RMSE = np.array(RMSE_list)
print(RMSE)
print(np.shape(RMSE))
print(np.shape(states))

df = pd.DataFrame(RMSE)
file_path_RMSE = os.path.join(file_path, "RMSE_velocity.txt")
df.to_csv(file_path_RMSE, sep=',', index=False, header=False, encoding='ascii', float_format='%.16f')