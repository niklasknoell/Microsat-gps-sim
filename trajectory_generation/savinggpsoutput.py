import serial

# Open a serial connection
ser = serial.Serial('CM04', 115200)  # Use the appropriate port and baud rate

# Specify the file path where you want to save the data
file_path = 'GPS_raw.txt'

# Open the file in write mode
with open(file_path, 'w') as file:
    #Save data to the file
    data = ser.readline()
    print('Received:', data)

    # Write the received data to the file
    file.write(data)

# Close the serial connection
ser.close()