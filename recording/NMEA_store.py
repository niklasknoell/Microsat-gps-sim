import serial
from datetime import datetime 
from pathlib import Path
import pynmea2



port = serial.Serial('COM4', baudrate=115200)

filename = datetime.now().strftime('Logs/NMEALog_%Y_%m_%d_%H_%M.log')

logFile = Path(filename)
logFile.parent.mkdir(parents=True, exist_ok=True)

file = logFile.open("+ab", buffering=64)
timeout = 80

while True:
    line = port.readline()
    if line[0] != 36:
        print(line[0])
        print(type(line[0]))
        continue
    file.write(bytearray(line))
    msg = pynmea2.parse(line.decode("utf-8"))
    print(msg)
    
    if msg.sentence_type == 'GSA':
        print(msg.data[1])
        timeout -= 1
        if msg.data[1] == '1' and timeout < 1:
            # Send out hot restart message
            timeout = 30
            print('Sending out hot restart')
            msg = bytearray(b'\xA0\xA1\x00\x0F\x01\x01\x07\xD8\x0B\x0E\x08\x2E\x03\x09\xC4\x30\x70\x00\x64\x16\x0D\x0A')
            port.write(msg)