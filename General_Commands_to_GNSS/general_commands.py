import serial


def send_receive_hex_message(serial_port, hex_message):
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

        # Convert the hex string to bytes
        byte_message = bytes.fromhex(hex_message)

        # Write the bytes to the serial port
        ser.write(byte_message)

        # Read the response from the serial port
        response = ser.read(100)  # Adjust the number of bytes to read based on your use case

        # Close the serial port
        ser.close()

        print(f"Hex message sent: {hex_message}")
        print(f"Received response (Hex): {response.hex()}")
    except Exception as e:
        print(f"Error: {e}")



def message_output_type(serial_port):
    # Structure: <0xA0,0xA1><PL><09><message body><CS><0x0D,0x0A>
    # Example: A0 A1 00 03 09 00 00 09 0D 0A
    # Field 1 - Message ID
    # Field 2 - Type: 00-No Output; 01-NMEA Message; 02-Binary Message
    # Field 3 - Attributes: 0-Update to SRAM; 1-Update to Both SRAM & FlASH

    output_type = input(print("Choose the output type (NMEA/BINARY): "))
    if output_type == "NMEA":
        hex_message = "A0A10003090000090D0A"  # Example Hex message
        send_receive_hex_message(serial_port, hex_message)
    elif output_type == "BINARY":
        hex_message = "A0A10003090200090D0A"  # Example Hex message
        send_receive_hex_message(serial_port, hex_message)
    else:
        print("Invalid output type")


def message_choice(serial_port):
    type_choice = str(input("Please choose if you want to choose output type (TRUE/FALSE): "))
    if type_choice.upper() == "TRUE":
        message_output_type(serial_port)
    else:
        print("Choice of Output Type declined")

# Replace 'COM1' with the appropriate serial port
message_choice('COM1')