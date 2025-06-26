import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

# Suppress SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Step 1: Define base URL
base_url = "https://www2.census.gov/programs-surveys/popest/tables/1980-1990/state/asrh/"

# Step 2: Create target folders
os.makedirs("ByStates", exist_ok=True)
os.makedirs("ByStatesWithAge", exist_ok=True)

# Step 3: Get HTML and parse links
html = requests.get(base_url, verify=False).text  # Still use requests just to scrape the page
soup = BeautifulSoup(html, "html.parser")

# Step 4: Compile regex patterns
pattern_st4 = re.compile(r"^st\d{4}\.txt$", re.IGNORECASE)
pattern_stiag = re.compile(r"^stiag.*\.txt$", re.IGNORECASE)

# Step 5: Process all .txt links
txt_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.txt')]

for filename in txt_links:
    filename = filename.strip()
    
    # Determine target folder
    if pattern_st4.match(filename):
        folder = "ByStates"
    elif pattern_stiag.match(filename):
        folder = "ByStatesWithAge"
    else:
        continue  # skip other files

    # Construct full download URL and local path
    file_url = urljoin(base_url, filename)
    output_path = os.path.join(folder, filename)

    # Download using curl
    print(f"Downloading {filename} to {output_path} ...")
    exit_code = os.system(f'curl -s -o "{output_path}" "{file_url}"')
    
    if exit_code != 0:
        print(f"⚠️ Failed to download {filename}")

print("✅ Download complete.")
