import requests
import csv
import io
from datetime import datetime

# URL of the CSV file
url = 'https://www.rba.gov.au/statistics/tables/csv/f11.1-data.csv'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the CSV content
    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(csv_content))
    
    # Skip rows until the row starting with "Series ID" is found
    data_array = []
    header_found = False
    for row in csv_reader:
        if header_found:
            # Change the format of the first column from dd-MMM-yyyy to yyyy-mm-dd
            try:
                row[0] = datetime.strptime(row[0], '%d-%b-%Y').strftime('%Y-%m-%d')
            except ValueError:
                continue  # Skip rows with invalid date format            
            data_array.append(row[:2])
        elif row and row[0].startswith("Series ID"):
            header_found = True

    # Read the existing rates.csv file
    with open('rates.csv', 'r') as rates_file:
        rates_reader = csv.reader(rates_file)
        rates_data = list(rates_reader)
        rates_first_column = {row[0] for row in rates_data}

    # Find rows in data_array where the first column value doesn't exist in rates.csv
    new_rows = [row for row in data_array if row[0] not in rates_first_column]

    # Append the new rows to rates.csv
    with open('rates.csv', 'a', newline='') as rates_file:
        rates_writer = csv.writer(rates_file)
    #    rates_writer.writerow([])
        rates_writer.writerows(new_rows)

    # find and remove all empty rows at the end of rates.csv
    with open('rates.csv', 'r') as rates_file:
        lines = rates_file.readlines()
    while lines[-1].strip() == "":
        lines.pop()
    with open('rates.csv', 'w') as rates_file:
        rates_file.writelines(lines)

    print(f"Added {len(new_rows)} new rows to rates.csv.")
else:
    print(f"Failed to download file. Status code: {response.status_code}")