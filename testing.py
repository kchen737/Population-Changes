import os

# Create folder if it doesn't exist
os.makedirs("ByStatesWithAge", exist_ok=True)

# URL and output path
url = "https://www2.census.gov/programs-surveys/popest/tables/1980-1990/state/asrh/stiag480.txt"
output_path = "ByStatesWithAge/stiag480.txt"

# Use curl to download
exit_code = os.system(f'curl -s -o "{output_path}" "{url}"')

if exit_code == 0:
    print("File downloaded successfully to", output_path)
else:
    print("Curl failed. Check internet or URL.")