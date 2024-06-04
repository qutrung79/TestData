import csv
import requests

# Replace 'your_api_url' with the actual API URL (without placeholder)
# Replace 'data_column' with the name of the column containing the data for the API call
def process_response(data, response_json):
  """
  Processes the JSON response and extracts relevant data.

  Args:
      data: The value used in the API call.
      response_json: The parsed JSON response object.

  Returns:
      A dictionary with keys 'summary', 'extracted_text', and 'data' (the original value).
  """
  result = {}
  result['summary'] = response_json.get('summary')  # Extract summary field
  result['extracted_text'] = []
  keywords = ["Given", "And", "When", "Then"]
  for line in response_json.get('text', []):  # Handle potential missing 'text' field
    if any(keyword in line for keyword in keywords):
      result['extracted_text'].append(line.strip())
  result['data'] = data
  return result

def call_api_and_store(data):
  url = f'{your_api_url}/{data}'
  response = requests.get(url)
  if response.status_code == 200:
    response_json = response.json()
    processed_data = process_response(data, response_json)
    return processed_data
  else:
    print(f'Error for {data}: {response.status_code}')
    return None  # Indicate error or handle missing data differently

def write_to_csv(data):
  with open('output.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Original Data', 'Summary', 'Description'])
    # Write header row if the file is empty
    if csvfile.tell() == 0:
      writer.writeheader()
    writer.writerow(data)

# Replace 'your_csv_file.csv' with the path to your CSV file
with open('your_csv_file.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)  # Skip header row if necessary
  all_data = []

  for row in reader:
    data = row[data_column]
    processed_data = call_api_and_store(data)
    if processed_data:  # Check if API call was successful
      all_data.append(processed_data)

# Write processed data to a new CSV file (output.csv)
for data in all_data:
  write_to_csv(data)

print('Processed data written to output.csv')
