import base64
import requests
import pandas as pd

GITHUB_TOKEN = "your_github_token_here"
REPO_OWNER = "aharon-tests"
REPO_NAME = "my_code"
BRANCH = "main"  # or "master"

def upload_file_to_github(local_file_path: str, github_file_path: str):
    # Read file content
    with open(local_file_path, "rb") as f:
        content = f.read()

    encoded_content = base64.b64encode(content).decode("utf-8")

    # Check if file already exists (to get its SHA for update)
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{github_file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    sha = None
    check_response = requests.get(api_url, headers=headers)
    if check_response.status_code == 200:
        sha = check_response.json().get("sha")

    # Prepare payload
    payload = {
        "message": f"Upload {github_file_path}",
        "content": encoded_content,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha  # Required for updating existing file

    # Upload file
    response = requests.put(api_url, headers=headers, json=payload)

    if response.status_code in (200, 201):
        print(f"✅ Success! File '{github_file_path}' uploaded to {REPO_OWNER}/{REPO_NAME} on branch '{BRANCH}'.")
        print(f"   View it at: https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH}/{github_file_path}")
    else:
        print(f"❌ Upload failed: {response.status_code} - {response.json().get('message')}")
        return

    # Print top and bottom 5 rows (assumes CSV or text file)
    try:
        df = pd.read_csv(local_file_path)
        print("\n--- Top 5 rows ---")
        print(df.head(5).to_string(index=False))
        print("\n--- Bottom 5 rows ---")
        print(df.tail(5).to_string(index=False))
    except Exception:
        # Fallback for non-CSV files
        lines = content.decode("utf-8", errors="replace").splitlines()
        print("\n--- Top 5 rows ---")
        print("\n".join(lines[:5]))
        print("\n--- Bottom 5 rows ---")
        print("\n".join(lines[-5:]))


if __name__ == "__main__":
    local_path = "path/to/your/file.csv"       # Local file path
    github_path = "folder/your_file.csv"        # Path inside the repo

    upload_file_to_github(local_path, github_path)