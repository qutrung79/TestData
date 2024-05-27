import os
import csv
import re

# Define input and output directories
input_directory = 'path/to/your/text/files'  # Replace this with the directory containing your text files
output_file = 'processed_data.csv'

# Constants for CSV columns
CSV_COLUMNS = ['Memory', 'Summary', 'ID']

# Initialize data list to hold extracted data
data = []

# Regex pattern to capture multi-line scenarios
scenario_regex = r"Beautifull:\s*(.+?)(?=\b(Given|You|Come|And)\b|$)"

# Function to extract scenario name and description from text
def extract_data(file_path, text):
    path = file_path
    description = []
    summary = None

    # Find all scenario matches using regex
    scenario_matches = re.findall(scenario_regex, text, re.DOTALL)

    # Split text by lines for further processing
    lines = text.split('\n')
    current_scenario_index = 0

    for i, line in enumerate(lines):
        line = line.strip()

        # Extract "Scenario" value after ":"
        if line.startswith('Scenario:'):
            if current_scenario_index < len(scenario_matches):
                scenario_value = scenario_matches[current_scenario_index][0].replace("\n", " ").strip()
                current_scenario_index += 1
            else:
                scenario_value = ''
            summary = scenario_value
            description = []

            if summary:  # If there's an existing scenario, append it first
                data.append({'PATH': path, 'Summary': summary, 'Description': '\n'.join(description)})

        # Collect lines starting with "Given", "And", "Then", or "When" as description
        elif any(line.startswith(keyword) for keyword in ['Given', 'And', 'Then', 'When']):
            description.append(line)

    # Append the last scenario data to the data list
    if summary:
        data.append({'PATH': path, 'Summary': summary, 'Description': '\n'.join(description)})

try:
    # Process each text file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as text_file:
                text_data = text_file.read()
                extract_data(file_path, text_data)

    # Write extracted data to CSV file
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Data has been written to {output_file}")

except Exception as e:
    print(f"Error occurred: {e}")
