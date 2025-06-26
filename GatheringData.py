import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL
base_url = "https://www2.census.gov/programs-surveys/popest/tables/1980-1990/state/asrh/"

# Create folders
os.makedirs("ByStates", exist_ok=True)
os.makedirs("ByStatesWithAge", exist_ok=True)

# Fetch the HTML content
response = requests.get(base_url, verify=False)

soup = BeautifulSoup(response.text, "html.parser")

# Find all .txt links
txt_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.txt')]

# Patterns
pattern_by_states = re.compile(r"^st\d{4}\*.txt$")
pattern_by_states_with_age = re.compile(r"^stiag.*\.txt$")

# Process each link
for link in txt_links:
    filename = link.lower()  # Ensure case-insensitive match

    # Match by pattern
    if pattern_by_states.match(filename):
        folder = "ByStates"
    elif pattern_by_states_with_age.match(filename):
        folder = "ByStatesWithAge"
    else:
        continue  # Skip files that don't match either

    # Download the file
    file_url = urljoin(base_url, link)
    local_path = os.path.join(folder, os.path.basename(link))

    print(f"Downloading {file_url} to {local_path}...")
    file_data = requests.get(file_url)
    with open(local_path, 'wb') as f:
        f.write(file_data.content)

print("Download complete.")
