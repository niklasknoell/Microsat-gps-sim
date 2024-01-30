#    Message Format
# Start of Sequence   Payload Length      Message ID      Message Body                Checksum (CS)       End of Sequence
# 0xA0, 0xA1          Two Bytes           1 bytes         Payload up to 65535 bytes   One bytes           0x0D, 0x0A

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


def message_choice(serial_port):


