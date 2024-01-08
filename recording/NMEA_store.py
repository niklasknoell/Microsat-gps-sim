import serial
from datetime import datetime 
from pathlib import Path



port = serial.Serial('COM4', baudrate=115200)

filename = datetime.now().strftime('Logs/NMEALog_%Y_%m_%d_%H_%M.log')

logFile = Path(filename)
logFile.parent.mkdir(parents=True, exist_ok=True)

file = logFile.open("+ab", buffering=64)

while True:
    line = port.readline()
    
    file.write(bytearray(line))
    
    print(line)