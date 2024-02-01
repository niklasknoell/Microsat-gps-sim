from datetime import datetime, timedelta
import pytz
import re
import os

# Specify the input and output directories
input_directory = '/binary_parsing/output_data'
output_directory = '/processing'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Get a list of all files in the input directory
input_files = [f for f in os.listdir(input_directory) if f.endswith('.log')]

# Iterate through each input file
for file_name in input_files:
    # Create the full path for the input and output files
    input_file_path = os.path.join(input_directory, file_name)
    output_file_path = os.path.join(output_directory, file_name[:-4] + '_post.txt')

    # Open the input file for processing
    with open(input_file_path, 'r') as file:
        lines = [line.strip() for line in file]

    result_string = '\n'.join(lines)

    split_strings = result_string.split("{\"status\":")

    if split_strings:
        split_strings.pop(0)

    final_strings = [sub_string.split('\"') for sub_string in split_strings]

    initial_time = float(re.sub(r"[^0-9.]", "", final_strings[0][21]))
    start_time = initial_time

    with open(output_file_path, 'w') as txtfile:
        for i in range(len(final_strings)):
            if final_strings[i][9] == '3D':
                first_lock = i
                break

    # Function for converting GPS time to datetime
    def gps_datetime(time_week, time_ms, leap_seconds=18):
        gps_epoch = datetime(1980, 1, 6, tzinfo=pytz.utc)
        return gps_epoch + timedelta(weeks=time_week, milliseconds=time_ms, seconds=-leap_seconds)

    # Open the text file for writing
    with open(output_file_path, 'w') as txtfile:
        for i in range(len(final_strings)):
            if final_strings[i][1] == 'complete' and final_strings[i][9] == '3D':
                gps_sec = (re.sub(r"[^0-9.]", "", final_strings[i][21]))
                time = (float(gps_sec) - 51840000) / 100
                x = float((re.sub(r"[^0-9.-]", "", final_strings[i][60]))) / 100
                y = float((re.sub(r"[^0-9.-]", "", final_strings[i][62]))) / 100
                z = float((re.sub(r"[^0-9.-]", "", final_strings[i][64]))) / 100
                vx = float((re.sub(r"[^0-9.-]", "", final_strings[i][66]))) / 100
                vy = float((re.sub(r"[^0-9.-]", "", final_strings[i][68]))) / 100
                vz = float((re.sub(r"[^0-9.-]", "", final_strings[i][70]))) / 100
            else:
                continue
            # Write the data to the text file without the header
            txtfile.write(f"{time}, {x}, {y}, {z}, {vx}, {vy}, {vz}\n")

    print(f"Data from {file_name} (without header) has been written to {output_file_path}")
