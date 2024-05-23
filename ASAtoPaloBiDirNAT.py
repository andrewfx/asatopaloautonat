import re

def parse_cisco_nat(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    nat_entries = []
    i = 0

    while i < len(lines):
        if lines[i].startswith('object network'):
            object_network_line = lines[i].strip()
            nat_statement_line = lines[i + 1].strip()

            nat_entries.append((object_network_line, nat_statement_line))
            i += 2
        else:
            i += 1
    
    return nat_entries

def generate_palo_alto_nat(nat_entries):
    palo_alto_commands = []

    for object_network_line, nat_statement_line in nat_entries:
        object_name = object_network_line.split()[-1]
        match_static = re.search(r'nat \((.*?),(.*?)\) static (.*)', nat_statement_line)
        match_dynamic = re.search(r'nat \((.*?),(.*?)\) dynamic (.*)', nat_statement_line)

        if match_static:
            outside_interface, inside_interface, static_object = match_static.groups()

            # Generate Palo Alto commands for the original static NAT statement
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" source-translation static-ip bi-directional no')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" source-translation static-ip translated-address {static_object}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" to {outside_interface}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" from {inside_interface}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" source {object_name}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" destination any')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" service any')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" to-interface any')

            # Generate Palo Alto commands for the reverse static NAT statement
            reversed_object_name = f"Cl AutoNat {object_name}"
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" source-translation static-ip bi-directional no')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" source-translation static-ip translated-address {object_name}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" to {inside_interface}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" from {outside_interface}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" source {static_object}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" destination any')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" service any')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "{reversed_object_name}" to-interface any')

        elif match_dynamic:
            outside_interface, inside_interface, dynamic_object = match_dynamic.groups()

            # Generate Palo Alto commands for the dynamic NAT statement
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" source-translation dynamic-ip-and-port translated-address {dynamic_object}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" to {outside_interface}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" from {inside_interface}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" source {object_name}')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" destination any')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" service any')
            palo_alto_commands.append(f'set vsys vsys1 rulebase nat rules "AutoNat {object_name}" to-interface any')

    return palo_alto_commands

def write_output(output_file, commands):
    with open(output_file, 'w') as file:
        for command in commands:
            file.write(command + '\n')

def main():
    input_file = 'input_nat_statements.txt'
    output_file = 'palo_alto_nat_statements.txt'

    # Parse the Cisco NAT statements
    nat_entries = parse_cisco_nat(input_file)
    
    # Generate the corresponding Palo Alto NAT commands
    palo_alto_commands = generate_palo_alto_nat(nat_entries)
    
    # Write the output to a file
    write_output(output_file, palo_alto_commands)
    print(f"Palo Alto NAT statements written to {output_file}")

if __name__ == "__main__":
    main()
