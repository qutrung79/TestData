import csv
import json
import requests

def csv_to_json(csv_file_path, json_file_path):
    # Prepare the JSON data
    json_data = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
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
    
    # Write the JSON data to a file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    return json_file_path

def import_tests(csv_file_path, json_file_path, api_url, token):
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    
    # Prepare the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Send the POST request
    response = requests.post(api_url, headers=headers, json=json_data)
    
    # Check the response
    if response.status_code == 200:
        print("Import successful!")
        test_id = response.json().get('test_id')  # Assuming the test ID is returned as 'test_id' in the response
        if test_id:
            # Update CSV with test ID
            update_csv(csv_file_path, test_id)
            print(f"Test ID {test_id} written to CSV.")
        else:
            print("Test ID not found in the response.")
    else:
        print(f"Failed to import. Status code: {response.status_code}")
        print(response.text)

def update_csv(csv_file_path, test_id):
    # Read CSV file
    rows = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames
        for row in reader:
            rows.append(row)
    
    # Update CSV data with test ID
    for row in rows:
        if test_id == row['summary'] or test_id == row['Description'] or test_id == row['xray_test_repository_folder']:
            row['Test ID'] = test_id
    
    # Write updated data back to CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers + ['Test ID'])
        writer.writeheader()
        writer.writerows(rows)

# Example usage
csv_file_path = 'data.csv'  # Path to your input CSV file
json_file_path = 'output.json'  # Path to your output JSON file
api_url = 'https://xray.cloud.getxray.app/api/v1/import/test/bulk'  # API endpoint
token = 'your_access_token'  # Replace with your actual token

# Convert CSV to JSON
json_file_path = csv_to_json(csv_file_path, json_file_path)

# Import JSON data via API
import_tests(csv_file_path, json_file_path, api_url, token)
