import tkinter as tk
from tkinter import simpledialog
from general_commands import *

# Instantiate the SerialPort class
my_serial_port = SerialPort()

# Function Related to the Button for Serial Port Configuration
def serial_port_config(root):  # Pass 'root' as a parameter
    # Create a new window for serial port configuration
    config_window = tk.Toplevel(root)
    config_window.title("Serial Port Configuration")

    # Labels and Entry widgets for serial port parameters
    serial_port = tk.Label(config_window, text="Write the Serial Port Name (e.g. COM1):")
    serial_port.grid(row=0, column=0, padx=5, pady=5)
    serial_port_entry = tk.Entry(config_window)
    serial_port_entry.grid(row=0, column=1, padx=5, pady=5)

    serial_port_speed = tk.Label(config_window, text="Write Down the Serial Port Speed:")
    serial_port_speed.grid(row=1, column=0, padx=5, pady=5)
    serial_port_speed_entry = tk.Entry(config_window)
    serial_port_speed_entry.grid(row=1, column=1, padx=5, pady=5)

    # Button to apply the serial port configuration
    apply_button = tk.Button(config_window, text="Apply",
                             command=lambda: apply_serial_config(root, serial_port_entry.get(), serial_port_speed_entry.get()))
    apply_button.grid(row=2, column=0, columnspan=2, pady=10)


def apply_serial_config(root, serial_port, serial_port_speed):
    # Use the entered serial port configuration
    print(f"Configuring serial port: Port={serial_port}, Baud Rate={serial_port_speed}")

    # Set serial port and speed
    my_serial_port.serial_port = serial_port
    my_serial_port.serial_port_speed = serial_port_speed

    # Here you can add the actual logic to configure the serial port using the provided parameters
    message_serial_port_config(my_serial_port, serial_port, serial_port_speed)


# Function Related to the Button for .......
def output_config(root):
    # Create a new window for serial port configuration
    config_window = tk.Toplevel(root)
    config_window.title("Output Choice")

    # Labels and Entry widgets for serial port parameters
    output_choice = tk.Label(config_window, text="Choose between NMEA and Binary output: ")
    output_choice.grid(row=0, column=0, padx=5, pady=5)
    output_choice_entry = tk.Entry(config_window)
    output_choice_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to apply the serial port configuration
    apply_button = tk.Button(config_window, text="Apply",
                             command=lambda: apply_output_config(root, output_choice_entry.get()))
    apply_button.grid(row=2, column=0, columnspan=2, pady=10)

def apply_output_config(root, output_choice_entry):
    message_output_type(my_serial_port, output_choice_entry)
    return


# Function Related to the Button for .......
def function_for_button_3():
    print("Button 3 clicked!")


# Function Related to the Button for .......
def function_for_button_4():
    print("Button 4 clicked!")


# Function Related to the Button for .......
def function_for_button_5():
    print("Button 5 clicked!")


# Function Related to the Button for .......
def function_for_button_6():
    print("Button 6 clicked!")


# Function Related to the Button for .......
def function_for_button_7():
    print("Button 7 clicked!")


# Function Related to the Button for .......
def function_for_button_8():
    print("Button 8 clicked!")


# Function Related to the Button for .......
def function_for_button_9():
    print("Button 9 clicked!")


# Function Related to the Button for .......
def function_for_button_10():
    print("Button 10 clicked!")

def create_gui():
    root = tk.Tk()
    root.title("Button GUI")

    # Create buttons with different names and assign distinct functions
    button_info = [
        {"name": "Serial Port Config", "function": lambda: serial_port_config(root)},
        {"name": "Output Choice", "function": lambda: output_config(root)},
        {"name": "N/A", "function": function_for_button_3},
        {"name": "N/A", "function": function_for_button_4},
        {"name": "N/A", "function": function_for_button_5},
        {"name": "N/A", "function": function_for_button_6},
        {"name": "N/A", "function": function_for_button_7},
        {"name": "N/A", "function": function_for_button_8},
        {"name": "N/A", "function": function_for_button_9},
        {"name": "N/A", "function": function_for_button_10},
    ]

    buttons = []
    for button_data in button_info:
        button = tk.Button(root, text=button_data["name"], command=button_data["function"])
        buttons.append(button)

    # Use the grid geometry manager to arrange buttons in 4 columns
    for i, button in enumerate(buttons):
        row_number = i // 4
        col_number = i % 4
        button.grid(row=row_number, column=col_number, padx=5, pady=5)

    root.mainloop()

# Create and run the GUI
create_gui()
