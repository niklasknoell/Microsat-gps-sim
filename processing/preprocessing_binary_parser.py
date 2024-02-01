file_path = "BINARYLog_2024_01_28_22_31_GEOS_noiono.log"  # Replace with the path to your text file

with open(file_path, 'r') as file:
    lines = file.readlines()

# Strip newline characters from each line
lines = [line.strip() for line in lines]

# Iterate through the lines and concatenate lines that do not start with "a0a1003" to the previous line
concatenated_lines = []
previous_line = ""

for line in lines:
    if line.startswith("a0a1003"):
        # If the current line starts with "a0a1003", add it to the list
        concatenated_lines.append(line)
        previous_line = line
    elif previous_line:
        # If the current line does not start with "a0a1003", add it to the previous line
        previous_line += line
        concatenated_lines[-1] = previous_line.replace(" ", "")  # Update the last element in the list, removing spaces

# Write the concatenated lines to a new text file
output_file_path = "BINARYLog_2024_01_28_22_31_GEOS_noiono_Repaired.txt"

with open(output_file_path, 'w') as output_file:
    for line in concatenated_lines:
        output_file.write(line + '\n')