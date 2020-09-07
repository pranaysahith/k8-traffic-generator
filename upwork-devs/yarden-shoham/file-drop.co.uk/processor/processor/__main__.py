import os
import requests
import urllib.request

jwt_token = os.getenv("API_TOKEN")
url = os.getenv("API_URL")
target = os.getenv("TARGET")

local_filename, _ = urllib.request.urlretrieve(target)

# Send a file to Glasswall's Rebuild API
with open(local_filename, "rb") as f:
    response = requests.post(
        url=url,
        files=[("file", f)],
        headers={
            "Authorization": jwt_token,
            "accept": "application/octet-stream"
        }
    )

output_file_path = f"/output/{os.path.basename(local_filename)}"

if response.status_code == 200 and response.content:
    # Glasswall has now sanitised and returned this file
    # Write the sanitised file to output file path
    with open(output_file_path, "wb") as f:
        f.write(response.content)
    print("Successfully wrote file to:", os.path.abspath(output_file_path))
else:
    # An error occurred, raise it
    response.raise_for_status()
