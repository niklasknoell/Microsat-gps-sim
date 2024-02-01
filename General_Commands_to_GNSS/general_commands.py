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
        ser = serial.Serial(serial_port, baudrate=115200, timeout=1)

        # Convert the hex string to bytes
        byte_message = bytes.fromhex(hex_message)

        # Write the bytes to the serial port
        ser.write(byte_message)

        # Read the response from the serial port
        response = receive_variable_response()  # Adjust the number of bytes to read based on your use case

        # Close the serial port
        ser.close()

        print(f"Hex message sent: {hex_message}")
        print(f"Received response (Hex): {response.hex()}")
    except Exception as e:
        print(f"Error: {e}")

def receive_variable_response(ser):
    start_message = ser.read(4)
    payload_length_hex = start_message[-2:].hex()
    payload_length_decimal = int(payload_length_hex, 16)
    message_payload_and_end = ser.read(payload_length_decimal + 3)
    total_message = start_message + message_payload_and_end

    return total_message


def message_ask_position_update_rate(serial_port_instance): #page23
    hex_message = "A0A10003090000090D0A"  # Example Hex message
    send_receive_hex_message(serial_port_instance.serial_port, hex_message)


def message_serial_port_config(serial_port, serial_port_speed):

    hex_message = "0xA0A1000405000100050D0A" # Unfinished Hex Message
    send_receive_hex_message(serial_port, hex_message)

def message_output_type_BINARY(serial_port):

    hex_message = "A0A100030902000B0D0A" # Hex message with correct CS for Binary output
    send_receive_hex_message(serial_port, hex_message)

def message_output_type_NMEA(serial_port):

    hex_message = "A0A10003090100080D0A" # Hex message with correct CS for Binary output
    send_receive_hex_message(serial_port, hex_message)

def messaqe_query_elevation_angle(serial_port):

    hex_message = "A0A100012F2F0D0A"
    send_receive_hex_message(serial_port, hex_message)

def message_configure_elevation15(serial_port):

    hex_message = "A0A100052B020F0000260D0A"
    send_receive_hex_message(serial_port, hex_message)

def message_configure_elevation_zero(serial_port):

    hex_message = "A0A100052B02000000290D0A"
    send_receive_hex_message(serial_port, hex_message)

ans = input(print("Please choose the ouput type, NMEA, BINARY, QUERYELEV, CONFELEV15, CONFELEVZERO:"))
if ans.upper() == "BINARY":
    message_output_type_BINARY("COM4")
    print("BINARY")
if ans.upper() == "NMEA":
    message_output_type_NMEA("COM4")
    print("NMEA")
if ans.upper() == "QUERYELEV":
    messaqe_query_elevation_angle("COM4")
    print("QUERYELEV")
if ans.upper() == "CONFELEV15":
    message_configure_elevation15("COM4")
    print("CONFELEV15")
if ans.upper() == "CONFELEVZERO":
    message_configure_elevation_zero("COM4")
    print("CONFELEVZERO")

