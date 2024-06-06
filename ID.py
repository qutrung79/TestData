import csv
import os
import re

# Define the folder containing the text files
input_folder = 'path/to/input_folder'  # Replace with your actual folder path

# Function to read file content
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to write new content to file
def write_file_content(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Regular expression to match the "Scenario" line
scenario_pattern = re.compile(r'^(Scenario\s*:)(.*)', re.MULTILINE)

# Read the input CSV file
with open('input.csv', newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        test_id = row['Test ID']
        summary = row['Summary']
        description = row['Description']

        # Combine summary and description for comparison
        combined_csv_content = f"{summary}\n{description}"

        # Iterate through text files in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)
                
                # Read the content of the text file
                file_content = read_file_content(file_path)
                
                # Compare the combined CSV content with the text file content
                if combined_csv_content in file_content:
                    # Search for the Scenario line and append Test ID to it
                    def append_test_id(match):
                        scenario_intro = match.group(1)  # "Scenario :"
                        existing_value = match.group(2).strip()  # The current scenario value
                        # Add Test ID right after "Scenario :"
                        new_value = f" [TEST - {test_id}] {existing_value}"
                        return f"{scenario_intro}{new_value}"
                    
                    new_content = scenario_pattern.sub(append_test_id, file_content)
                    
                    # Write the new content back to the file if any replacement was made
                    if new_content != file_content:
                        write_file_content(file_path, new_content)
                        print(f"Updated file {filename} with new scenario: [TEST - {test_id}] {summary}")

print("Processing completed.")
