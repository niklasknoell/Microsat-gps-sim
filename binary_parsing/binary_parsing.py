import os
import json
import numpy as np

def translate_line(line):
    # This code makes the assumption that the binaty message is saved in the text file in Hex
    line = line.strip()
    # Sectioning the data in the message
    message_body = line[8:-6]
    translation = {}
    hex_line = {"total": line, "message_body": message_body}

    # Message ID
    message_id = message_body[0:2]
    translation["Message_ID"] = message_id
    hex_line["message_id"]= message_id

    # Fix Mode Interpretation
    fix_mode = message_body[2:4]
    fix_mode_meaning = translate_fix_mode_section(fix_mode)
    translation["Fix_Mode"] = fix_mode_meaning
    hex_line["fix_mode"]= fix_mode

    # Number of SV in fix
    SV_number = message_body[4:6]
    sv_decimal = translate_sv_number(SV_number)
    translation["SV_Number"] = sv_decimal
    hex_line["SV_number"]= SV_number

    # GNSS week number
    gnss_week = message_body[6:10]
    gnss_week_decimal = translate_GNSS_week(gnss_week)
    translation["GNSS_Week"] = gnss_week_decimal
    hex_line["gnss_week"]= gnss_week

    # TOW interpretation
    TOW_hex = message_body[10:18]
    TOW_decimal = translate_TOW(TOW_hex)
    translation["TOW"] = TOW_decimal
    hex_line["TOW_hex"]= TOW_hex

    # Latitude Translation
    latitude_hex = message_body[18:26]
    latitude_decimal = hex_to_decimal_latitude(latitude_hex)
    translation["Latitude"] = latitude_decimal
    hex_line["latitude_hex"]= latitude_hex

    # Longitude Translation
    longitude_hex = message_body[26:34]
    longitude_decimal = hex_to_decimal_longitude(longitude_hex)
    translation["Longitude"] = longitude_decimal
    hex_line["longitude_hex"]= longitude_hex

    # Ellipsoid Altitude Translation
    ellipsoid_hex = message_body[34:42]
    ellipsoid_decimal = hex_to_decimal_ellipsoid(ellipsoid_hex)
    translation["Ellipsoid_Altitude"] = ellipsoid_decimal
    hex_line["ellipsoid_hex"]= ellipsoid_hex

    # Mean Sea Level Altitude
    sea_altitude_hex = message_body[42:50]
    sea_altitude_decimal = hex_to_decimal_sea_level_altitude(sea_altitude_hex)
    translation["Sea_Level_Altitude"] = sea_altitude_decimal
    hex_line["sea_altitude_hex"]= sea_altitude_hex

    # GDOP Translation
    GDOP_hex = message_body[50:54]
    GDOP_decimal = hex_to_decimal_GDOP(GDOP_hex)
    translation["GDOP"] = GDOP_decimal
    hex_line["GDOP_hex"]= GDOP_hex

    # PDOP Translation
    PDOP_hex = message_body[54:58]
    PDOP_decimal = hex_to_decimal_PDOP(PDOP_hex)
    translation["PDOP"] = PDOP_decimal
    hex_line["PDOP_hex"]= PDOP_hex

    # HDOP Translation
    HDOP_hex = message_body[58:62]
    HDOP_decimal = hex_todecimal_HDOP(HDOP_hex)
    translation["HDOP"] = HDOP_decimal
    hex_line["HDOP_hex"]= HDOP_hex

    # VDOP Translation
    VDOP_hex = message_body[62:66]
    VDOP_decimal = hex_to_decimal_VDOP(VDOP_hex)
    translation["VDOP"] = VDOP_decimal
    hex_line["VDOP_hex"]= VDOP_hex

    # TDOP Translation
    TDOP_hex = message_body[66:70]
    TDOP_decimal = hex_to_decimal_TDOP(TDOP_hex)
    translation["TDOP"] = TDOP_decimal
    hex_line["TDOP_hex"]= TDOP_hex

    # ECEF-X Translation
    ECEFX_hex = message_body[70:78]
    ECEFX_decimal = hex_to_decimal_ECEFX(ECEFX_hex)
    translation["ECEFX"] = ECEFX_decimal
    hex_line["ECEFX_hex"]= ECEFX_hex

    # ECEF-Y Translation
    ECEFY_hex = message_body[78:86]
    ECEFY_decimal = hex_to_decimal_ECEFY(ECEFY_hex)
    translation["ECEFY"] = ECEFY_decimal
    hex_line["ECEFY_hex"]= ECEFY_hex

    # ECEF-Z Translation
    ECEFZ_hex = message_body[86:94]
    ECEFZ_decimal = hex_to_decimal_ECEFZ(ECEFZ_hex)
    translation["ECEFZ"] = ECEFZ_decimal
    hex_line["ECEFZ_hex"]= ECEFZ_hex

    # ECEF-VX Translation
    ECEFVX_hex = message_body[94:102]
    ECEFVX_decimal = hex_to_decimal_ECEFVX(ECEFVX_hex)
    translation["ECEF-VX"] = ECEFVX_decimal
    hex_line["ECEFVX_hex"]= ECEFVX_hex

    # ECEF-VY Translation
    ECEFVY_hex = message_body[102:110]
    ECEFVY_decimal = hex_to_decimal_ECEFVY(ECEFVY_hex)
    translation["ECEF-VY"] = ECEFVY_decimal
    hex_line["ECEFVY_hex"]= ECEFVY_hex

    # ECEF-VZ Translation
    ECEFVZ_hex = message_body[110:118]
    ECEFVZ_decimal = hex_to_decimal_ECEFVZ(ECEFVZ_hex)
    translation["ECEF-VZ"] = ECEFVZ_decimal
    hex_line["ECEFVZ_hex"]= ECEFVZ_hex

    print(hex_line)

    return translation

def translate_fix_mode_section(fix_mode):
    fix_mode_meaning = ""
    if fix_mode == "00":
        fix_mode_meaning = "no_fix"
    if fix_mode == "01":
        fix_mode_meaning = "2D"
    if fix_mode == "02":
        fix_mode_meaning = "3D"
    if fix_mode == "03":
        fix_mode_meaning = "3D+DGNSS"
    return fix_mode_meaning

def translate_sv_number(sv_number):
    if sv_number:
        decimal_value = int(str(sv_number), 16)
        return str(decimal_value)
    else:
        return 'N/A'

def translate_GNSS_week(gnss_week_hex):
    if gnss_week_hex:
        decimal_value = int(str(gnss_week_hex), 16)
        return str(decimal_value)
    return 'N/A'

def translate_TOW(tow_hex):
    if tow_hex:
        decimal_value = np.uint32(int(tow_hex, 16))
        return str(decimal_value)
    else:
        # Handle the case where tow_hex is empty (return a default value or raise an exception)
        return "N/A"  # Replace with your desired default value or appropriate handling


def hex_to_decimal_latitude(hex_value):
    if hex_value:
        # Convert hex to decimal for sint32
        decimal_value = int(hex_value, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        # Determine if it is in the North or South Hemisphere
        if decimal_value > 0:
            latitude = str(decimal_value) + "N"
        else:
            latitude = str(decimal_value) + "S"
        return latitude
    else:
        # Handle the case where latitude_hex is empty (return a default value or raise an exception)
        return "N/A"  # Replace with your desired default value or appropriate handling


def hex_to_decimal_longitude(hex_value):
    if hex_value:
    # Convert hex to decimal for sint32
        decimal_value = int(hex_value, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        # Determine if it is in the East or West Hemisphere
        if decimal_value > 0:
            longitude = str(decimal_value) + "E"
        else:
            longitude = str(decimal_value) + "W"
        return longitude
    else:
        # Handle the case where longitude_hex is empty (return a default value or raise an exception)
        return "N/A"  # Replace with your desired default value or appropriate handling

def hex_to_decimal_ellipsoid(hex_value):
    if hex_value:
        # Convert hex to decimal
        decimal_value = int(hex_value, 16)
        return str(decimal_value)
    else:
        # Handle the case where hex_value is empty (return a default value or raise an exception)
        return "N/A"  # Replace with your desired default value or appropriate handling


def hex_to_decimal_sea_level_altitude(sea_altitude_hex):
    if sea_altitude_hex:
        # Convert hex to decimal
        decimal_value = int(sea_altitude_hex, 16)
        return str(decimal_value)
    else:
        # Handle the case where sea_altitude_hex is empty (return a default value or raise an exception)
        return "N/A"  # Replace with your desired default value or appropriate handling


def hex_to_decimal_GDOP(GDOP_hex):
    if GDOP_hex:
        decimal_value = int(GDOP_hex, 16)
        return str(decimal_value)
    else:
        return "N/A"

def hex_to_decimal_PDOP(PDOP_hex):
    if PDOP_hex:
        decimal_value = int(PDOP_hex, 16)
        return str(decimal_value)
    else:
        return "N/A"

def hex_todecimal_HDOP(HDOP_hex):
    if HDOP_hex:
        decimal_value = int(HDOP_hex, 16)
        return str(decimal_value)
    else:
        return "N/A"

def hex_to_decimal_VDOP(VDOP_hex):
    if VDOP_hex:
        decimal_value = int(VDOP_hex, 16)
        return str(decimal_value)
    else:
        return "N/A"

def hex_to_decimal_TDOP(TDOP_hex):
    if TDOP_hex:
        decimal_value = int(TDOP_hex, 16)
        return str(decimal_value)
    return 'N/A'

def hex_to_decimal_ECEFX(ECEFX_hex):
    if ECEFX_hex:
        # Convert hex to decimal for sint32
        decimal_value = int(ECEFX_hex, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        return decimal_value
    else:
        return 'N/A'

def hex_to_decimal_ECEFY(ECEFY_hex):
    if ECEFY_hex:
        # Convert hex to decimal for sint32
        decimal_value = int(ECEFY_hex, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        return decimal_value
    else:
        return 'N/A'

def hex_to_decimal_ECEFZ(ECEFZ_hex):
    if ECEFZ_hex:
        # Convert hex to decimal for sint32
        decimal_value = int(ECEFZ_hex, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        return decimal_value
    else:
        return 'N/A'

def hex_to_decimal_ECEFVX(ECEFVX_hex):
    if ECEFVX_hex:
        # Convert hex to decimal for sint32
        decimal_value = int(ECEFVX_hex, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        return decimal_value
    else:
        return 'N/A'

def hex_to_decimal_ECEFVY(ECEFVY_hex):
    if ECEFVY_hex:
        # Convert hex to decimal for sint32
        decimal_value = int(ECEFVY_hex, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        return decimal_value
    else:
        return 'N/A'

def hex_to_decimal_ECEFVZ(ECEFVZ_hex):
    if ECEFVZ_hex:
        # Convert hex to decimal for sint32
        decimal_value = int(ECEFVZ_hex, 16)

        # If the value is negative, apply two's complement to get the correct signed value
        if decimal_value & (1 << 31):
            decimal_value -= 1 << 32

        return decimal_value
    else:
        return 'N/A'





def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def translate_and_save(input_file, output_file, save_original):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Use the translate_line function to translate each line
            translated_line = translate_line(line)

            # Also save the original line in the new file
            if save_original:
                outfile.write(f"Original: {line.strip()}\nTranslated: {translated_line}\n")
            # Only save the translated line
            else:
                outfile.write(f"{json.dumps(translated_line)}\n")

def process_files(input_directory, output_directory, save_original):
    # Ensure the output directory exists
    create_directory(output_directory)

    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, f"processed_parsed_{filename}")

        translate_and_save(input_file_path, output_file_path, save_original)

# Replace 'input_directory' and 'output_directory' with your input and output directories
input_directory = 'input_data'
output_directory = 'output_data'
save_original = False

process_files(input_directory, output_directory, save_original)

