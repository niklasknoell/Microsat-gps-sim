import os
import json


def translate_line(line):
    # This code makes the assumption that the binaty message is saved in the text file in Hex
    line = line.strip()
    # Sectioning the data in the message
    message_body = line[8:-6]
    translation = {}

    # Message ID
    message_id = message_body[0:1]
    translation["Message_ID"] = message_id

    # Fix Mode Interpretation
    fix_mode = message_body[2:3]
    fix_mode_meaning = translate_fix_mode_section(fix_mode)
    translation["Fix_Mode"] = fix_mode_meaning

    # Number of SV in fix
    SV_number = message_body[4:5]
    sv_decimal = translate_sv_number(SV_number)
    translation["SV_Number"] = sv_decimal

    # GNSS week number
    gnss_week = message_body[6:9]
    gnss_week_decimal = translate_GNSS_week(gnss_week)
    translation["GNSS_Week"] = gnss_week_decimal

    # TOW interpretation
    TOW_hex = message_body[10:17]
    TOW_decimal = translate_TOW(TOW_hex)
    translation["TOW"] = TOW_decimal

    # Latitude Translation
    latitude_hex = message_body[18:25]
    latitude_decimal = hex_to_decimal_latitude(latitude_hex)
    translation["Latitude"] = latitude_decimal

    # Longitude Translation
    longitude_hex = message_body[26:33]
    longitude_decimal = hex_to_decimal_longitude(longitude_hex)
    translation["Longitude"] = longitude_decimal

    # Ellipsoid Altitude Translation
    ellipsoid_hex = message_body[34:41]
    ellipsoid_decimal = hex_to_decimal_ellipsoid(ellipsoid_hex)
    translation["Ellipsoid_Altitude"] = ellipsoid_decimal

    # Mean Sea Level Altitude
    sea_altitude_hex = message_body[42:49]
    sea_altitude_decimal = hex_to_decimal_sea_level_altitude(sea_altitude_hex)
    translation["Sea_Level_Altitude"] = sea_altitude_decimal

    # GDOP Translation
    GDOP_hex = message_body[50:53]
    GDOP_decimal = hex_to_decimal_GDOP(GDOP_hex)
    translation["GDOP"] = GDOP_decimal

    # PDOP Translation
    PDOP_hex = message_body[54:57]
    PDOP_decimal = hex_to_decimal_PDOP(PDOP_hex)
    translation["PDOP"] = PDOP_decimal

    # HDOP Translation
    HDOP_hex = message_body[58:61]
    HDOP_decimal = hex_todecimal_HDOP(HDOP_hex)
    translation["HDOP"] = HDOP_decimal

    # VDOP Translation
    VDOP_hex = message_body[62:65]
    VDOP_decimal = hex_to_decimal_VDOP(VDOP_hex)
    translation["VDOP"] = VDOP_decimal

    # TDOP Translation
    TDOP_hex = message_body[66:69]
    TDOP_decimal = hex_to_decimal_TDOP(TDOP_hex)
    translation["TDOP"] = TDOP_decimal

    # ECEF-X Translation
    ECEFX_hex = message_body[70:77]
    ECEFX_decimal = hex_to_decimal_ECEFX(ECEFX_hex)
    translation["ECEFX"] = ECEFX_decimal

    # ECEF-Y Translation
    ECEFY_hex = message_body[78:85]
    ECEFY_decimal = hex_to_decimal_ECEFY(ECEFY_hex)
    translation["ECEFX"] = ECEFY_decimal

    # ECEF-Z Translation
    ECEFZ_hex = message_body[86:93]
    ECEFZ_decimal = hex_to_decimal_ECEFZ(ECEFZ_hex)
    translation["ECEFX"] = ECEFZ_decimal

    # ECEF-VX Translation
    ECEFVX_hex = message_body[94:101]
    ECEFVX_decimal = hex_to_decimal_ECEFVX(ECEFVX_hex)
    translation["ECEF-VX"] = ECEFVX_decimal

    # ECEF-VY Translation
    ECEFVY_hex = message_body[102:109]
    ECEFVY_decimal = hex_to_decimal_ECEFVY(ECEFVY_hex)
    translation["ECEF-VY"] = ECEFVY_decimal

    # ECEF-VZ Translation
    ECEFVZ_hex = message_body[110:117]
    ECEFVZ_decimal = hex_to_decimal_ECEFVZ(ECEFVZ_hex)
    translation["ECEF-VZ"] = ECEFVZ_decimal

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
        decimal_value = int(str(tow_hex), 16)
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

