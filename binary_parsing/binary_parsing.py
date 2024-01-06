    Message Format

Start of Sequence   Payload Length      Message ID      Message Body                Checksum (CS)       End of Sequence
0xA0, 0xA1          Two Bytes           1 bytes         Payload up to 65535 bytes   One bytes           0x0D, 0x0A


<0xA0,0xA1><PL><Message ID><Message Body><CS><0x0D,0x0A>





# Replace this function with your own translation method
def translate_line(line):
    # This code makes the assumption that the binaty message is saved in the text file in Hex
    line = line.strip()
    # Sectioning the data in the message
    message_body = line[8:-6]
    translation = ""

    # Message ID
    message_id = message_body[0:1]

    # Fix Mode Interpretation
    fix_mode = message_body[2:3]
    fix_mode_meaning = translate_fix_mode_section(fix_mode)
    translation += fix_mode_meaning

    # Number of SV in fix
    SV_number = message_body[4:5]
    sv_decimal = translate_sv_number(SV_number)
    translation += sv_decimal

    # GNSS week number
    gnss_week = message_body[6:9]

    # Placeholder: return the original line if no translation method is provided
    return line

def translate_fix_mode_section(fix_mode):
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
    decimal_value = int(str(sv_number), 16)
    return str(decimal_value)

def hex_to_decimal_latitude(hex_value):
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

def hex_to_decimal_longitude(hex_value):
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

def translate_and_save(input_file, output_file, save_original):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Use the translate_line function to translate each line
            translation = translate_line(line)

            # Also save the original line in the new file
            if save_original == True:
                outfile.write(f"Original: {line.strip()}\nTranslated: {translation.strip()}\n\n")
            # Only the save the translated line
            if save_original == False:
                outfile.write(f"{translation.strip()}\n\n")

# DDecide if you want to save the origianl line or not
save_original = False


# Replace 'input.txt' and 'output.txt' with your input and output file names
# Optionally, specify the target language (e.g., 'es' for Spanish, 'fr' for French)
translate_and_save('input.txt', 'output.txt', save_original)
