import csv

input_file_path = 'output_NMEA_data.txt'  # Replace with the path to your CSV file
output_file_path = 'NMEAmrcleantime.txt'  # Replace with the desired path for the new CSV file

with open(input_file_path, 'r', newline='') as infile, open(output_file_path, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write headers to the output file
    headers = next(reader)
    writer.writerow(headers)

    # Filter and write rows with no empty strings
    for row in reader:
        if all(cell.strip() for cell in row):  # Check if all cells are non-empty after stripping whitespace
            writer.writerow(row)

print(f"Filtered CSV written to {output_file_path}")