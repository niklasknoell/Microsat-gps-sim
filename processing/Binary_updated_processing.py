from datetime import datetime, timedelta
import pytz
import re

file_path = 'processed_parsed_BINARYLog_2024_01_28_21_11_GEOS_Default_Settings_Repaired.txt'
output_file_path = 'processed_parsed_BINARYLog_2024_01_28_21_11_GEOS_Default_Settings_Repaired_Post.txt'

with open(file_path, 'r') as file:
    lines = [line.strip() for line in file]

result_string = '\n'.join(lines)
#print(result_string)

split_strings = result_string.split("{\"status\":")

if split_strings:
    split_strings.pop(0)

final_strings = [sub_string.split('\"') for sub_string in split_strings]

initial_time = float(re.sub(r"[^0-9.]", "", final_strings[0][21]))
start_time = initial_time

def gps_datetime(time_week, time_ms, leap_seconds=18):
    gps_epoch = datetime(1980, 1, 6, tzinfo=pytz.utc)
    return gps_epoch + timedelta(weeks=time_week, 
                                 milliseconds=time_ms, 
                                 seconds=-leap_seconds)

# Open the text file for writing
with open(output_file_path, 'w') as txtfile:
    for i in range(len(final_strings)):
        if final_strings[i][1] == 'complete':
            #gps_week = (re.sub(r"[^0-9.]", "", final_strings[i][17]))
            gps_sec = (re.sub(r"[^0-9.]", "", final_strings[i][21]))
            #if not gps_week:
            #    time = 'N/A'
            #elif not gps_sec:
            #    time = 'N/A'
            #else:
            time = (float(gps_sec)-float(final_strings[416][21]))/100+416
            x = float((re.sub(r"[^0-9.-]", "", final_strings[i][60])))/100
            y = float((re.sub(r"[^0-9.-]", "", final_strings[i][62])))/100
            z = float((re.sub(r"[^0-9.-]", "", final_strings[i][64])))/100
            vx = float((re.sub(r"[^0-9.-]", "", final_strings[i][66])))/100
            vy = float((re.sub(r"[^0-9.-]", "", final_strings[i][68])))/100
            vz = float((re.sub(r"[^0-9.-]", "", final_strings[i][70])))/100
        else:
            time = 'incomplete'
            x = 'incomplete'
            y = 'incomplete'
            z = 'incomplete'
            vx = 'incomplete'
            vy = 'incomplete'
            vz = 'incomplete'
        # Write the data to the text file without the header
        txtfile.write(f"{time}, {x}, {y}, {z}, {vx}, {vy}, {vz}\n")

print(f"Data (without header) has been written to {output_file_path}")