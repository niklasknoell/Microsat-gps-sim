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

while True:
    line = port.readline()
    hex_line = line.hex()
    file.write(hex_line.encode('utf-8') + b'\n')
