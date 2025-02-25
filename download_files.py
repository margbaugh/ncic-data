import os
from pathlib import Path
import requests
import csv

# Path to the CSV file with URLs
csv_file = 'metadata.csv'

# Folder to save the downloaded files
save_folder = 'downloaded_files'

# Create a folder to save files if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Read the CSV file and download the files
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    header = next(reader, None)
    
    # Assuming the CSV has headers and URL links are in the first column
    for row in reader:
        if row:  # Check if the row is not empty
            file_url = row[1]  # Adjust this if the URL is in a different column

            # Extract the filename from the URL (using the file name from the URL itself)
            filename = os.path.join(save_folder, os.path.basename(file_url))
            file = Path(filename)
            if file.exists():
                continue
            
            try:
                # Send a GET request to download the file
                response = requests.get(file_url)
                
                # Check if the request was successful
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download {file_url}. HTTP Status: {response.status_code}")
            except Exception as e:
                print(f"Error downloading {file_url}: {e}")
