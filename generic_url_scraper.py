import requests
from bs4 import BeautifulSoup

import hashlib
import re
import urllib.parse
import os

def get_links_from_url(url, filter=None, save_html=True):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <a> tags and extract the href attribute
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Save copy of page
        response.raise_for_status()  # Ensure the request was successful

        # Save the HTML content to a file
        filename = url_to_filename(url)
        # Get the current working directory
        current_directory = os.getcwd()

        # Create the full file path in the current directory
        if save_html:
            file_path = os.path.join(current_directory, filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)

            print(f"Page saved as {file_path}")
        
        # return full links, not relative ones
        full_links = [urllib.parse.urljoin(url, link) for link in links]

        # If there is a filter for the links to return, apply now
        if not filter:
            return full_links
        filtered_links = set()
        for link in full_links:
            if filter in link:
                filtered_links.add(link)
        return filtered_links
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []


def save_html(url, filename):
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Save the HTML content to a file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)

        print(f"Page saved as {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")


def url_to_filename(url):
    # Parse the URL to remove the protocol (http:// or https://)
    parsed_url = urllib.parse.urlparse(url)
    
    # Get the netloc (domain) and path (the rest of the URL)
    netloc = parsed_url.netloc
    path = parsed_url.path

    # Combine netloc and path for the filename
    raw_filename = netloc + path
    
    # Replace any non-alphanumeric characters with underscores
    raw_filename = re.sub(r'[^a-zA-Z0-9]', '_', raw_filename)

    # Return the final unique filename (using the hash as a unique part)
    filename = f"files/{raw_filename}.html"  # You can adjust the extension based on your need
    return filename





