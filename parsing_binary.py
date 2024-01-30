def binary_parser(message):
    tot_msg = message.split('<')
    while("" in tot_msg):
        tot_msg.remove("")
    for idx, ele in enumerate(tot_msg):
        tot_msg[idx] = ele.replace('>', '')
    return (tot_msg)

def parse_binary(sentence):
    msg = binary_parser(sentence)
    return str(msg)  # Convert the parsed message object to a string
    

def process_binary_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('$'):
                parsed_data = parse_binary(line.strip())
                if parsed_data:
                    # Save both the original sentence and the parsed data
                    if original == True:
                        outfile.write(f"Original: {line.strip()}\nParsed: {parsed_data}\n\n")
                    if original == False:
                        outfile.write(f"{parsed_data}\n")

# Change if desired to also save the original or not
original = False

# Replace 'input.txt' and 'output.txt' with your input and output file names
process_binary_file('input.txt', 'output.txt')