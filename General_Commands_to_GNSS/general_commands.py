import serial



# This class is used to store the Serial Port Characteristics, such as COM and Speed
class SerialPort:
    def __init__(self):
        self._serial_port = None
        self._serial_port_speed = None

    @property
    def serial_port(self):
        return self._serial_port

    @serial_port.setter
    def serial_port(self, value):
        # You can add validation or additional logic here if needed
        self._serial_port = value

    @property
    def serial_port_speed(self):
        return self._serial_port_speed

    @serial_port_speed.setter
    def serial_port_speed(self, value):
        # You can add validation or additional logic here if needed
        self._serial_port_speed = value

    def get_serial_port(self):
        return self._serial_port

    def get_serial_port_speed(self):
        return self._serial_port_speed


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

def message_config_power_mode(serial_port_instance): #page20
    mode_option = input(print("""Please make a choice in Mode:
    00 = Normal (diasble)
    01 = Power Save (enable)"""))

    attribute_option = input(print("""Please make a choice in Attributes:
    00 = Update to SRAM
    01 = Update to both SRAM & FLASH
    02 = Temporarily enabled"""))

    if mode_option == "00":
        if attribute_option == "00":
            hex_message = "A0A1 0003 0C0000 09 0D0A"  # Implemented Hex Message
        if attribute_option == "01":
            hex_message = "A0A1 0003 0C0001 09 0D0A"  # Implemented Hex Message
        if attribute_option == "02":
            hex_message = "A0A1 0003 0C0002 09 0D0A"  # Implemented Hex Message
        send_receive_hex_message(serial_port_instance.serial_port, hex_message)
    if mode_option == "01":
        if attribute_option == "00":
            hex_message = "A0A1 0003 0C0100 09 0D0A"  # Implemented Hex Message
        if attribute_option == "01":
            hex_message = "A0A1 0003 0C0101 09 0D0A"  # Implemented Hex Message
        if attribute_option == "02":
            hex_message = "A0A1 0003 0C0102 09 0D0A"  # Implemented Hex Message
        send_receive_hex_message(serial_port_instance.serial_port, hex_message)

def message_update_rate_GNSS(): #page22
    rate_option = input(print("Unfinished")) # Not Understanding the Documentation


def message_ask_position_update_rate(serial_port_instance): #page23
    hex_message = "A0A10003090000090D0A"  # Example Hex message
    send_receive_hex_message(serial_port_instance.serial_port, hex_message)

def message_output_type(serial_port_instance, output_choice): # Output Selection
    # Structure: <0xA0,0xA1><PL><09><message body><CS><0x0D,0x0A>
    # Example: A0 A1 00 03 09 00 00 09 0D 0A
    # Field 1 - Message ID
    # Field 2 - Type: 00-No Output; 01-NMEA Message; 02-Binary Message
    # Field 3 - Attributes: 0-Update to SRAM; 1-Update to Both SRAM & FlASH

    output_option = input(print("""Please make a choice in Mode:
        NMEA
        BINARY"""))

    attribute_option = input(print("""Please make a choice in Attributes:
        00 = Update to SRAM
        01 = Update to both SRAM & FLASH
        02 = Temporarily enabled"""))

    if output_option.upper() == "NMEA":
        if attribute_option == "00":
            hex_message = "A0A1 0003 0C0000 09 0D0A"  # Implemented Hex Message
        if attribute_option == "01":
            hex_message = "A0A1 0003 0C0001 09 0D0A"  # Implemented Hex Message
        if attribute_option == "02":
            hex_message = "A0A1 0003 0C0002 09 0D0A"  # Implemented Hex Message
        send_receive_hex_message(serial_port_instance.get_serial_port(), hex_message)
    if output_option.upper() == "BINARY":
        if attribute_option == "00":
            hex_message = "A0A1 0003 0C0100 09 0D0A"  # Implemented Hex Message
        if attribute_option == "01":
            hex_message = "A0A1 0003 0C0101 09 0D0A"  # Implemented Hex Message
        if attribute_option == "02":
            hex_message = "A0A1 0003 0C0102 09 0D0A"  # Implemented Hex Message
        send_receive_hex_message(serial_port_instance.get_serial_port(), hex_message)
    else:
        print("Invalid output type")

def message_serial_port_config(serial_port_instance, serial_port, serial_port_speed):

    hex_message = "0xA0A1000405000100050D0A" # Unfinished Hex Message
    send_receive_hex_message(serial_port_instance.get_serial_port(), hex_message)



# def message_choice(serial_port):
#
#     # This part is to configure the Serial port to the desired port
#     serial_config = str(input("Please tell if you wish to change the serial port config (YES/NO): "))
#     if serial_config.upper() == "TRUE":
#         serial_port_choice = str(input("Please write the serial port name (e.g. COM1): "))
#         message_serial_port_config(serial_port_choice)
#     else:
#         print("Serial Port Config Declined")
#
#     # This part is to decide the output type between NMEA and Binary
#     type_choice = str(input("Please choose if you want to choose output type (TRUE/FALSE): "))
#     if type_choice.upper() == "TRUE":
#         message_output_type(serial_port)
#     else:
#         print("Choice of Output Type declined")
#
# # Replace 'COM1' with the appropriate serial port
# message_choice('COM1')