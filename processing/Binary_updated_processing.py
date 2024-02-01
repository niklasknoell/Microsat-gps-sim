from datetime import datetime, timedelta
import pytz
import re
import os
import glob

# Specify the directory containing the .log files
directory_path = '/binary_parsing/output_data'

# Use glob to get a list of all .log files in the directory
log_files = glob.glob(os.path.join(directory_path, '*.log'))

# Iterate through each .log file and open it
for log_file in log_files:
    with open(log_file, 'r') as file:
        lines = [line.strip() for line in file]
        result_string = '\n'.join(lines)
        #print(result_string)
        
        split_strings = result_string.split("{\"status\":")
        
        if split_strings:
            split_strings.pop(0)
        
        final_strings = [sub_string.split('\"') for sub_string in split_strings]
        
        initial_time = float(re.sub(r"[^0-9.]", "", final_strings[0][21]))
        start_time = initial_time
        
        with open(output_file_path, 'w') as txtfile:
            for i in range(len(final_strings)):
                if final_strings[i][9]=='3D':
                    first_lock=i
                    break
        
        def gps_datetime(time_week, time_ms, leap_seconds=18):
            gps_epoch = datetime(1980, 1, 6, tzinfo=pytz.utc)
            return gps_epoch + timedelta(weeks=time_week, 
                                         milliseconds=time_ms, 
                                         seconds=-leap_seconds)
        
        # Open the text file for writing
        with open(output_file_path, 'w') as txtfile:
            for i in range(len(final_strings)):
                if final_strings[i][1] == 'complete' and final_strings[i][9] == '3D':
                    #gps_week = (re.sub(r"[^0-9.]", "", final_strings[i][17]))
                    gps_sec = (re.sub(r"[^0-9.]", "", final_strings[i][21]))
                    #if not gps_week:
                    #    time = 'N/A'
                    #elif not gps_sec:
                    #    time = 'N/A'
                    #else:
                    #time = (float(gps_sec)-float(final_strings[first_lock][21]))/100+first_lock
                    time = (float(gps_sec)-51840000)/100
                    x = float((re.sub(r"[^0-9.-]", "", final_strings[i][60])))/100
                    y = float((re.sub(r"[^0-9.-]", "", final_strings[i][62])))/100
                    z = float((re.sub(r"[^0-9.-]", "", final_strings[i][64])))/100
                    vx = float((re.sub(r"[^0-9.-]", "", final_strings[i][66])))/100
                    vy = float((re.sub(r"[^0-9.-]", "", final_strings[i][68])))/100
                    vz = float((re.sub(r"[^0-9.-]", "", final_strings[i][70])))/100
                else:
                    continue
                # Write the data to the text file without the header
                txtfile.write(f"{time}, {x}, {y}, {z}, {vx}, {vy}, {vz}\n")

        output_file_path=os.path.join(output_directory, os.path.basename(log_file)[:-4] + '_post.log')
        print(f"Data (without header) has been written to {output_file_path}")

    

    
