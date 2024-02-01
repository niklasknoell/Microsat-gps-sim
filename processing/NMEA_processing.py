from datetime import datetime, timedelta
import pytz
import re

file_paths = ['parsed_NMEALog_2024_01_09_14_49.log.txt']
output_file_path = 'output_NMEA_data.txt'

lines_list=[]

for file_path in file_paths:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        lines_list.extend(lines)

final_strings = [sub_string.split(',') for sub_string in lines_list]

initial_time = final_strings[264][0].replace('Timestamp: ', '')
test=initial_time.split(':')
test1=test[2].replace('+00','')
start_time=float(test1)+float(test[0])*3600+float(test[1])*60
#start_time = initial_time

#def gps_datetime(time_week, time_ms, leap_seconds=18):
#    gps_epoch = datetime(1980, 1, 6, tzinfo=pytz.utc)
#    return gps_epoch + timedelta(weeks=time_week, 
#                                 milliseconds=time_ms, 
#                                 seconds=-leap_seconds)

# Open the text file for writing
with open(output_file_path, 'w') as txtfile:
    for i in range(len(final_strings)):
        #gps_week = (re.sub(r"[^0-9.]", "", final_strings[i][17]))
        #gps_sec = (re.sub(r"[^0-9.]", "", final_strings[i][21]))
        #if not gps_week:
        #    time = 'N/A'
        #elif not gps_sec:
        #    time = 'N/A'
        #else:
        #print(i)
        time0 = final_strings[i][0]
        time = time0.replace('Timestamp: ', '')
        if not time:
            time=''
        else:
            time1=time.split(':')
            time4=time1[2].replace('+00','')
            time=float(time4)+float(time1[0])*3600+float(time1[1])*60-start_time+23.627663
        Latitude = (re.sub(r"[^0-9.]", "", final_strings[i][1]))
        if not Latitude:
            Latitude=''
        else:
            if final_strings[i][1][-1] == 'S':
                Latitude=-1*float(Latitude)
            else:
                Latitude=float(Latitude)
        Longitude = (re.sub(r"[^0-9.]", "", final_strings[i][2]))
        if not Longitude:
            Longitude=''
        else:
            if final_strings[i][2][-1] == 'W':
                Longitude=-1*float(Longitude)
            else:
                Longitude=float(Longitude)
        Altitude = (re.sub(r"[^0-9.]", "", final_strings[i][3]))
        if not Altitude:
            Altitude=''
        else:
            Altitude=float(Altitude)
        # Write the data to the text file without the header
        txtfile.write(f"{time}, {Latitude}, {Longitude}, {Altitude}\n")

print(f"Data (without header) has been written to {output_file_path}")
