import os
import pynmea2

def parse_nmea(sentence):
    try:
        msg = pynmea2.parse(sentence)
        return str(msg)  # Convert the parsed message object to a string
    except pynmea2.ParseError:
        return None

def process_nmea_directory(input_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, f"parsed_{filename}")

        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            for line in infile:
                if line.startswith('$'):
                    parsed_data = parse_nmea(line.strip())
                    if parsed_data:
                        # Save both the original sentence and the parsed data
                        if original == True:
                            outfile.write(f"Original: {line.strip()}\nParsed: {parsed_data}\n\n")
                        if original == False:
                            outfile.write(f"{parsed_data}\n")

# Change if desired to also save the original or not
original = False

# Specify the path to the input directory and output directory
input_directory = 'data'  # Adjust to your input directory
output_directory = 'output_data'  # Adjust to your output directory

process_nmea_directory("nmea_data", "parsed_nmea")

