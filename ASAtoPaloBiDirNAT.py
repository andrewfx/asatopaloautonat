import re

def reverse_nat_statements(input_file, output_file, output_format):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    output_lines = []
    i = 0

    while i < len(lines):
        if lines[i].startswith('object network'):
            object_network_line = lines[i].strip()
            nat_statement_line = lines[i + 1].strip()

            # Check if the NAT statement is static
            if 'static' in nat_statement_line and 'dynamic' not in nat_statement_line:
                # Extract the object names and directions
                match = re.search(r'nat \((.*?),(.*?)\) static (.*)', nat_statement_line)
                if match:
                    outside_interface, inside_interface, static_object = match.groups()

                    if output_format.lower() == 'cisco':
                        # Create the reverse NAT statement in Cisco ASA format
                        reversed_nat_statement = f"nat ({inside_interface},{outside_interface}) static {object_network_line.split()[-1]}"
                        output_lines.append(object_network_line)
                        output_lines.append(reversed_nat_statement)
                        output_lines.append(f"object network {static_object}")
                        output_lines.append(f"nat ({outside_interface},{inside_interface}) static {object_network_line.split()[-1]}")
                    elif output_format.lower() == 'palo alto':
                        # Create the reverse NAT statement in Palo Alto format
                        original_nat_rule = f"set nat rule {object_network_line.split()[-1]} from {outside_interface} to {inside_interface} source {static_object} destination any service any"
                        reversed_nat_rule = f"set nat rule {static_object} from {inside_interface} to {outside_interface} source {object_network_line.split()[-1]} destination any service any"
                        output_lines.append(original_nat_rule)
                        output_lines.append(reversed_nat_rule)

            i += 2  # Skip to the next pair of lines
        else:
            i += 1  # Move to the next line

    with open(output_file, 'w') as file:
        for line in output_lines:
            file.write(line + '\n')

def main():
    input_file = 'input_nat_statements.txt'
    output_file = 'reversed_nat_statements.txt'
    
    print("Choose the output format:")
    print("1. Cisco ASA CLI commands")
    print("2. Palo Alto CLI commands")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        output_format = 'cisco'
    elif choice == '2':
        output_format = 'palo alto'
    else:
        print("Invalid choice. Defaulting to Cisco ASA CLI commands.")
        output_format = 'cisco'

    reverse_nat_statements(input_file, output_file, output_format)

if __name__ == "__main__":
    main()
