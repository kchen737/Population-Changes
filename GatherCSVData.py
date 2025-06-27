import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

# Suppress SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ask user for the target URL
base_url = input("Enter the URL to download .csv files from: ").strip()

# Ensure it ends with a slash
if not base_url.endswith('/'):
    base_url += '/'

# Create folders
os.makedirs("2000age", exist_ok=True)
os.makedirs("2000race", exist_ok=True)

# Patterns to match filenames
pattern_age = re.compile(r'^st-est00int-02-\d{2}\.csv$', re.IGNORECASE)
pattern_race = re.compile(r'^st-est00int-03-\d{2}\.csv$', re.IGNORECASE)

# Download the HTML from the page
try:
    response = requests.get(base_url, verify=False)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("❌ Error fetching the URL:", e)
    exit(1)

# Parse HTML to get CSV links
soup = BeautifulSoup(response.text, "html.parser")
csv_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].lower().endswith('.csv')]

# Loop through and download matching files
for filename in csv_links:
    filename = filename.strip()
    
    if pattern_age.match(filename):
        folder = "2000age"
    elif pattern_race.match(filename):
        folder = "2000race"
    else:
        continue  # skip unmatched files

    file_url = urljoin(base_url, filename)
    output_path = os.path.join(folder, os.path.basename(filename))

    print(f"⬇️ Downloading {filename} to {folder}/ ...")
    exit_code = os.system(f'curl -s -o "{output_path}" "{file_url}"')

    if exit_code != 0:
        print(f"⚠️ Failed to download {filename}")

print("✅ All matching CSV files downloaded.")

