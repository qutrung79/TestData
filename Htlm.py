import csv
import os
import re
from bs4 import BeautifulSoup

# Define input and output file paths
input_folder_path = 'html_folder'  # Ensure this folder exists and contains your HTML files
output_file_path = 'processed_data.csv'

# Constants for new columns
LABELS = "message_bdd"
PRODUCTS_NAME = "SBE"
ISSUE_TYPE = "Xray Test"
POD_ENVIRONMENT = "QA"
ASSOCIATED_PROJECT = "Backend Core API"

# Open the output CSV file
with open(output_file_path, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    # Write the header to the CSV file
    csv_writer.writerow([
        'Summary', 'Description', 'Labels', 'Product(s) Name', 
        'Issue Type', 'Pod Environment', 'Associated Project', 'Repo'
    ])
    
    # Process each HTML file in the specified folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(input_folder_path, filename)
            print(f"Processing file: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as infile:
                soup = BeautifulSoup(infile, 'html.parser')
                text = soup.get_text()
                lines = text.splitlines()

                repo = ''
                summary = ''
                description = []
                
                for line in lines:
                    line = line.strip()
                    
                    if "Feature" in line:
                        # Extract the value after "/TestData/" and assign it to repo
                        match = re.search(r'/TestData/(.*)', line)
                        if match:
                            repo = match.group(1).strip()
                            print(f"Found repo: {repo}")
                    
                    if line.startswith('Scenario:'):
                        if summary and description:
                            # Write the previous scenario's data to the CSV
                            csv_writer.writerow([
                                summary, '\n'.join(description), LABELS, PRODUCTS_NAME, 
                                ISSUE_TYPE, POD_ENVIRONMENT, ASSOCIATED_PROJECT, repo
                            ])
                            print(f"Wrote scenario to CSV: {summary}")
                        
                        # Extract the summary text after "Scenario: "
                        summary = line.split('Scenario:')[-1].strip()
                        description = []
                        print(f"Found scenario: {summary}")

                    elif any(line.startswith(keyword) for keyword in ['Given', 'And', 'Then', 'When']):
                        description.append(line)
                        print(f"Added to description: {line}")

                # Write the last scenario's data to the CSV (if any)
                if summary and description:
                    csv_writer.writerow([
                        summary, '\n'.join(description), LABELS, PRODUCTS_NAME, 
                        ISSUE_TYPE, POD_ENVIRONMENT, ASSOCIATED_PROJECT, repo
                    ])
                    print(f"Wrote final scenario to CSV: {summary}")

print(f"Data has been written to {output_file_path}")
