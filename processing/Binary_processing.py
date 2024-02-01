from datetime import datetime, timedelta
import pytz
import re

file_path = 'Binary2024-01-22_165436 - Copy.out.txt'
output_file_path = 'output_data.txt'

with open(file_path, 'r') as file:
    lines = [line.strip() for line in file]

result_string = '\n'.join(lines)
#print(result_string)

split_strings = result_string.split("$fix mode=")

if split_strings:
    split_strings.pop(0)

final_strings = [sub_string.split('\n$') for sub_string in split_strings]

initial_time = float(re.sub(r"[^0-9.]", "", final_strings[0][3]))
start_time = initial_time -48

def gps_datetime(time_week, time_ms, leap_seconds=18):
    gps_epoch = datetime(1980, 1, 6, tzinfo=pytz.utc)
    return gps_epoch + timedelta(weeks=time_week, 
                                 milliseconds=time_ms, 
                                 seconds=-leap_seconds)

# Open the text file for writing
with open(output_file_path, 'w') as txtfile:
    for i in range(len(final_strings)):
        gps_week = float(re.sub(r"[^0-9.]", "", final_strings[i][2]))+100
        gps_sec = float(re.sub(r"[^0-9.]", "", final_strings[i][3]))*10**3+374429010+432000
        time = gps_datetime(gps_week, gps_sec)
        x = float(re.sub(r"[^0-9.]", "", final_strings[i][12]))
        y = float(re.sub(r"[^0-9.]", "", final_strings[i][13]))
        z = float(re.sub(r"[^0-9.]", "", final_strings[i][14]))
        vx = float(re.sub(r"[^0-9.]", "", final_strings[i][15]))
        vy = float(re.sub(r"[^0-9.]", "", final_strings[i][16]))
        vz = float(re.sub(r"[^0-9.]", "", final_strings[i][17]))

        # Write the data to the text file without the header
        txtfile.write(f"{time}, {x}, {y}, {z}, {vx}, {vy}, {vz}\n")

print(f"Data (without header) has been written to {output_file_path}")