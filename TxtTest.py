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

    for line in text.split('\n'):
        line = line.strip()
        
        # Extract "Scenario" value after ":"
        if line.startswith('Scenario:'):
            if summary:  # If there's an existing scenario, append it first
                data.append({'PATH': path, 'Summary': summary, 'Description': '\n'.join(description)})
            scenario_value = line.split(':', 1)[1].strip()
            summary = scenario_value
            description = []
        
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
