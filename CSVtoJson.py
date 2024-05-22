import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Prepare the JSON data
        json_data = []
        for row in csv_reader:
            json_data.append({
                "testtype": row['testtype'],
                "fields": {
                    "summary": row['summary'],
                    "Description": row['Description'],
                    "project": {"key": "CALC"}  # Assuming "CALC" is a constant value
                },
                "unstructured_def": "x.CalculatorTests.CanMultiply",  # Assuming this is a constant value
                "xray_test_repository_folder": row['xray_test_repository_folder']
            })
        
        # Add the additional testset definition
        json_data.append({
            "xray_issue_type": "testset"
        })
    
    # Write to JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4)

# Example usage
csv_file_path = 'data.csv'  # Path to your input CSV file
json_file_path = 'output.json'  # Path to your output JSON file

csv_to_json(csv_file_path, json_file_path)
