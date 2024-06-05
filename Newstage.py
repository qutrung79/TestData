import csv
import requests

# Define the new API base URL
api_base_url = 'https://api.example.com/data/'  # Replace with your actual API base URL

# Initialize a list to store the results
results = []

# Read the input CSV file
with open('input.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Skip the header row
    for row in csvreader:
        test_id = row[0]

        # Construct the API URL with the test ID
        api_url = f"{api_base_url}{test_id}"

        # Make the GET request to the new API
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract the 'summary' field
            summary = data.get('summary', 'No summary found')

            # Extract the 'text' fields that start with 'Given', 'And', 'When', 'Then'
            texts = [item for item in data.get('text', []) if item.startswith(('Given', 'And', 'When', 'Then'))]
            description = ' '.join(texts)

            # Append the result to the list
            results.append({
                'Test ID': test_id,
                'Summary': summary,
                'Description': description
            })
        else:
            print(f"Failed to retrieve data for Test ID {test_id}. Status code: {response.status_code}")

# Write the results to a new CSV file
with open('output_with_summary_and_description.csv', 'w', newline='') as csvfile:
    fieldnames = ['Test ID', 'Summary', 'Description']
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    csvwriter.writeheader()

    # Write the rows
    for result in results:
        csvwriter.writerow(result)

print("Values have been written to output_with_summary_and_description.csv")
