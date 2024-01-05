import os
import pynmea2


def clear_directory(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path):
        # Iterate over the files in the directory and remove them
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def parse_nmea(sentence):
    try:
        msg = pynmea2.parse(sentence)
        return msg  # Return the parsed message object
    except pynmea2.ParseError:
        return None

def full_parsed_nmea_directory(input_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, f"parsed_{filename}")

        with open(input_file_path, 'r') as infile, open(output_file_path, 'a') as outfile:
            for line in infile:
                if line.startswith('$'):
                    parsed_data = parse_nmea(line.strip())
                    if parsed_data:
                        # Create a dictionary to store information, labels, and units
                        nmea_info = {
                            'Timestamp': f"Timestamp: {getattr(parsed_data, 'timestamp', '')}",
                            'Latitude': f"Latitude: {getattr(parsed_data, 'lat', '')} {getattr(parsed_data, 'lat_dir', '')}",
                            'Longitude': f"Longitude: {getattr(parsed_data, 'lon', '')} {getattr(parsed_data, 'lon_dir', '')}",
                            'Altitude': f"Altitude: {getattr(parsed_data, 'altitude', '')} Meters",
                            'Speed_Over_Ground': f"Speed Over Ground: {getattr(parsed_data, 'speed_over_ground', '')} Knots",
                            'Date': f"Date: {getattr(parsed_data, 'date', '')}",
                            'GPS_Quality_Indicator': f"GPS Quality Indicator: {getattr(parsed_data, 'gps_qual', '')}",
                            'Number_of_Satellites': f"Number of Satellites: {getattr(parsed_data, 'num_sats', '')}",
                            # Add more components as needed
                        }

                        # Create an output line with labels, values, and units
                        output_line = ', '.join(value for value in nmea_info.values()) + '\n'
                        outfile.write(output_line)

def convert_coordinates(latitude, longitude, lat_direction, lon_direction):
    try:
        # Check if latitude and longitude values are not empty
        if latitude and longitude:
            # Convert latitude and longitude to decimal degrees
            lat_degrees = float(latitude[:2]) + float(latitude[2:]) / 60
            lon_degrees = float(longitude[:3]) + float(longitude[3:]) / 60

            # Apply direction for latitude and longitude
            if lat_direction == 'S':
                lat_degrees = -lat_degrees
            if lon_direction == 'W':
                lon_degrees = -lon_degrees

            return lat_degrees, lon_degrees
        else:
            # Return default values if latitude or longitude is empty
            return None, None
    except ValueError:
        # Return default values if conversion to float fails
        return None, None

def process_nmea_directory(input_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, f"parsed_{filename}")

        with open(input_file_path, 'r') as infile, open(output_file_path, 'a') as outfile:
            for line in infile:
                if line.startswith('$'):
                    parsed_data = parse_nmea(line.strip())
                    # Convert latitude and longitude to decimal degrees
                    lat_degrees, lon_degrees = convert_coordinates(
                        getattr(parsed_data, 'lat', ''),
                        getattr(parsed_data, 'lon', ''),
                        getattr(parsed_data, 'lat_dir', ''),
                        getattr(parsed_data, 'lon_dir', '')
                    )

                    # Extract all available information and append to the output file
                    components = {
                        'Timestamp': getattr(parsed_data, 'timestamp', ''),
                        'Latitude': f"{lat_degrees:.6f} degrees" if lat_degrees is not None else "Latitude: N/A",
                        'Longitude': f"{lon_degrees:.6f} degrees" if lon_degrees is not None else "Longitude: N/A",
                        'Altitude': f"{getattr(parsed_data, 'altitude', '')} Meters",
                        'Speed_Over_Ground': f"{getattr(parsed_data, 'speed_over_ground', '')} Knots",
                        'Date': getattr(parsed_data, 'date', ''),
                        # Add more components as needed
                    }

                    # Create an output line with labels
                    output_line = ', '.join(f"{label}: {value}" for label, value in components.items()) + '\n'
                    outfile.write(output_line)




# Specify the path to the input directory and output directory
input_directory = '_01_input_nmea_data'
output_directory = 'processed_parsed_nmea'
full_output_directory = 'parsed_full_nmea'

# Clear the contents of the directories
clear_directory(output_directory)
clear_directory(full_output_directory)

print("Contents cleared successfully.")

full_parsed_nmea_directory(input_directory, full_output_directory)
process_nmea_directory(input_directory, output_directory)

