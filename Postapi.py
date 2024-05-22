import json
import requests

def import_tests(json_file_path, api_url, token):
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
        print(response.json())
    else:
        print(f"Failed to import. Status code: {response.status_code}")
        print(response.text)

# Example usage
json_file_path = 'output.json'  # Path to your JSON file
api_url = 'https://xwey.cloud.weray.app/api/v1/iweort/twet/bwek'  # API endpoint
token = 'your_access_token'  # Replace with your actual token

import_tests(json_file_path, api_url, token)


