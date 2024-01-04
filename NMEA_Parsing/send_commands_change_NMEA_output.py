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




# def message_configure_NMEA_talker_ID():
#
#
#     return
#
# def message_choice(serial_port):
#
#
# # Configure the Serial port Property
# message_serial_port_config("COM1")
#
# # Replace 'COM1' with the appropriate serial port
# message_choice('COM1')
