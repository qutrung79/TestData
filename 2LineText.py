import os
import csv

# Define input and output directories
input_directory = 'path/to/your/text/files'  # Replace this with the directory containing your text files
output_file = 'processed_data.csv'

# Constants for CSV columns
CSV_COLUMNS = ['PATH', 'Summary', 'Description']

# Initialize data list to hold extracted data
data = []

# Function to extract scenario name and description from text
def extract_data(file_path, text):
    path = file_path
    summary = None
    description = []
    in_scenario = False

    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Extract "Scenario" value after ":"
        if line.startswith('Scenario:'):
            if summary:  # If there's an existing scenario, append it first
                data.append({'PATH': path, 'Summary': summary, 'Description': '\n'.join(description)})

            # Initialize summary with current line
            scenario_value = line.split(':', 1)[1].strip()
            summary_lines = [scenario_value] if scenario_value else []

            # Collect subsequent lines if they don't start with a keyword or another "Scenario:"
            while i + 1 < len(lines) and not any(lines[i + 1].strip().startswith(keyword) for keyword in ['Scenario:', 'Given', 'And', 'Then', 'When']):
                i += 1
                summary_lines.append(lines[i].strip())

            summary = ' '.join(summary_lines)
            description = []
            in_scenario = True
        
        # Collect lines starting with "Given", "And", "Then", or "When" as description
        elif in_scenario and any(line.startswith(keyword) for keyword in ['Given', 'And', 'Then', 'When']):
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
