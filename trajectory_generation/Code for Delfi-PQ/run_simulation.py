#------------------This file is used to run all code for the sensitivity analysis simulation of interest------------------#

import subprocess
import time

scripts = [
    "ECEF_to_ECI_conversion.py",
    "ECI_to_Keplerian_conversion.py",
    "error_kepler_elements.py",
    "RMSE.py",
    "RSW error.py",
    "position & velocity error.py",
    "error_quantification.py"
]

# Loop through the scripts and run them sequentially
for script in scripts:
    subprocess.run(["python", script], check=True)
    # time.sleep(5)  # Pause for 5 seconds before proceeding to the next script

