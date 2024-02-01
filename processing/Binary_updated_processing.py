from datetime import datetime, timedelta
import pytz
import re
import os

input_directory = 'binary_parsing/output_data'
output_directory = 'processing'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

def process_file(input_file_path, output_file_path):
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
            if final_strings[i][9]=='3D':
                first_lock=i
                break

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

                # Write the data to the text file without the header
                txtfile.write(f"{time}, {x}, {y}, {z}, {vx}, {vy}, {vz}\n")

    print(f"Data (without header) has been written to {output_file_path}")

# List all files in the input directory
files = os.listdir(input_directory)

for file in files:
    # Check if the file is a text file (you can adjust the condition based on your file types)
    if file.endswith('.txt'):
        input_file_path = os.path.join(input_directory, file)
        output_file_path = os.path.join(output_directory, f'{os.path.splitext(file)[0]}_post.txt')

        # Process the file and save the result with the "_post" suffix
        process_file(input_file_path, output_file_path)

print("Processing completed for all files.")
