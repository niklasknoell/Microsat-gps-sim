import serial
from datetime import datetime
from pathlib import Patch
import pynmea2


port = serial.Serial('COM4', baudrate=115200)

filename = datetime.now().strftime('Logs/BINARYLog_%Y_%m_%d_%H_%M.log')

logFile = Path(filename)
logFile.parent.mkdir(parents=True, exist_ok=True)

file = logFile.open("+ab", buffering=64)
timeout = 80

def saving_method1():
    while True:
        line = port.readline()
        hex_line = line.hex()
        file.write(hex_line.encode('utf-8') + b'\n')


def saving_method(port, file_path):
    with open(file_path, 'ab', buffering=0) as file:
        try:
            while True:
                start_message = port.read(4)
                payload_length_hex = start_message[-2:].hex()
                payload_length_decimal = int(payload_length_hex, 16)
                message_payload_and_end = port.read(payload_length_decimal + 3)
                total_message = start_message + message_payload_and_end
                total_message_hex = total_message.hex()
                file.write(total_message_hex.encode('utf-8') + b'\n')
                file.flush()  # Ensure data is immediately written to the file
        except Exception as e:
            print(f"An error occurred: {e}")


saving_method1()

