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


lat_lon_alt_GPS = np.genfromtxt(os.path.join(file_path,"NMEA.txt").replace("\\.", "."), delimiter=',')
# lat_lon_alt_GPS[:,0] += 1

initial_time = lat_lon_alt_GPS[0,0]
end_simulation = 10000
index = np.where(lat_lon_alt_GPS[:, 0] >= end_simulation)[0][0]
lat_lon_alt_GPS = lat_lon_alt_GPS[:index+1, :]


lat_GPS = lat_lon_alt_GPS[:,1]
lon_GPS = lat_lon_alt_GPS[:,2]
alt_GPS = lat_lon_alt_GPS[:,3]


lat_lon_alt = np.genfromtxt(os.path.join(file_path,"lat_lon_alt.txt").replace("\\.", "."), delimiter=',')
index = np.where(lat_lon_alt[:, 0] >= initial_time)[0][0]
lat_lon_alt = lat_lon_alt[index:,:]
lat_lon_alt = lat_lon_alt[::10]
index = np.where(lat_lon_alt[:, 0] >= end_simulation)[0][0]
lat_lon_alt = lat_lon_alt[:index+1, :]

lat = lat_lon_alt[:,1]
lon = lat_lon_alt[:,2]
alt = lat_lon_alt[:,3]



fig = plt.figure(figsize=(9, 5))
plt.title("Ground track of Delfi-PQ")
plt.scatter(lon, lat, s=30,label="Benchmark",marker="+")
plt.scatter(lon_GPS, lat_GPS, s=5,label="GNSS")
plt.xlabel('Longitude [deg]')
plt.ylabel('Latitude [deg]')
plt.xticks(np.arange(-180, 181, step=45))
plt.xlim(-180, 180)
plt.yticks(np.arange(-90, 91, step=45))
plt.grid()
plt.tight_layout()
plt.legend()

# Save file
output_path = os.path.join(figures_path,"ground track Delfi-PQ.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')


fig = plt.figure(figsize=(9, 5))
plt.title("Altitude over time of Delfi-PQ")
plt.scatter(lat_lon_alt[:,0], alt/1000, s=1,label="Benchmark")
plt.scatter(lat_lon_alt_GPS[:,0], alt_GPS/1000, s=5,label="GNSS")
# plt.scatter(lat_lon_alt[:,0],alt_GPS-alt)
plt.xlabel('time [s]')
plt.ylabel('altitude [km]')
plt.grid()
plt.tight_layout()
plt.legend()

# Save file
output_path = os.path.join(figures_path,"altitude over time Delfi-PQ.pdf").replace("\\.", ".")
fig.savefig(output_path, bbox_inches='tight')




plt.show()