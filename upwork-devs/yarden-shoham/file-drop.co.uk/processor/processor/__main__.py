import os
import requests

jwt_token = os.getenv("API_TOKEN")
url = "https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file"


for filename in os.listdir("/input"):
    # Send a file to Glasswall's Rebuild API
    with open(f"/input/{filename}", "rb") as f:
        response = requests.post(
            url=url,
            files=[("file", f)],
            headers={
                "Authorization": jwt_token,
                "accept": "application/octet-stream"
            }
        )

    output_file_path = f"/output/{filename}"

    if response.status_code == 200 and response.content:
        # Glasswall has now sanitised and returned this file
        # Write the sanitised file to output file path
        with open(output_file_path, "wb") as f:
            f.write(response.content)
        print("Successfully wrote file to:", os.path.abspath(output_file_path))
    else:
        # An error occurred, raise it
        response.raise_for_status()
