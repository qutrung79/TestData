import os
import csv
import re

# Define input and output directories
input_directory = 'path/to/your/text/files'  # Replace this with the directory containing your text files
output_file = 'processed_data.csv'
test_output_file = 'test_data.csv'

# Constants for CSV columns
CSV_COLUMNS = ['PATH', 'Summary', 'Description']

# Initialize data lists to hold extracted data
data = []
test_data = []

# Regular expression to capture multi-line scenario descriptions
regex = r"(?<=Scenario:\s)(?s).+?(?=\s+Given|\s+Then|\s+When|\s+And|\s+Scenario:|$)"
test_regex = r'\[TEST-[^\]]+\]'

# Function to extract scenario name and description from text
def extract_data(file_path, text):
    path = file_path
    description = []
    summary = None

    # Use regex to find all scenario matches
    scenario_matches = re.findall(regex, text)
    current_scenario_index = 0

    for line in text.split('\n'):
        line = line.strip()

        # Extract "Scenario" value after ":"
        if line.startswith('Scenario:'):
            if current_scenario_index < len(scenario_matches):
                scenario_value = scenario_matches[current_scenario_index].replace("\n", " ").strip()
                current_scenario_index += 1
            else:
                scenario_value = ''

            if 'TEST' in line:
                test_match = re.findall(test_regex, line)
                if test_match:
                    test_value = test_match[0].strip()
                    test_data.append({'PATH': path, 'Summary': test_value, 'Description': ''})
            else:
                if summary and description:  # If there's an existing scenario, append it first
                    data.append({'PATH': path, 'Summary': summary, 'Description': '\n'.join(description)})
                summary = scenario_value
                description = []

        # Collect lines starting with "Given", "And", "Then", or "When" as description
        elif any(line.startswith(keyword) for keyword in ['Given', 'And', 'Then', 'When']):
            description.append(line)

    # Append the last scenario data to the data list if it's not empty
    if summary and description:
        data.append({'PATH': path, 'Summary': summary, 'Description': '\n'.join(description)})

try:
    # Process each text file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as text_file:
                text_data = text_file.read()
                extract_data(file_path, text_data)

    # Write extracted data to CSV file without extra blank lines
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    # Write test scenario data to separate CSV file without extra blank lines
    with open(test_output_file, 'w', newline='') as test_csv_file:
        test_writer = csv.DictWriter(test_csv_file, fieldnames=CSV_COLUMNS)
        test_writer.writeheader()
        for test_row in test_data:
            test_writer.writerow(test_row)

    print(f"Data has been written to {output_file}")
    print(f"Test data has been written to {test_output_file}")

except Exception as e:
    print(f"Error occurred: {e}")
