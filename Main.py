import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')
WORKFLOW_ID = os.getenv('WORKFLOW_ID')

# Ensure all environment variables are set
if not all([GITHUB_TOKEN, REPO_OWNER, REPO_NAME, WORKFLOW_ID]):
    raise ValueError("One or more environment variables are missing.")

# GitHub API endpoints
workflow_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_ID}/runs"
trigger_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_ID}/dispatches"

# Headers for the API request
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Data to pass along with the trigger request (e.g., branch to trigger on)
data = {
    "ref": "main"  # The branch where the workflow should be triggered
}

def is_workflow_running():
    response = requests.get(workflow_url, headers=headers)
    if response.status_code == 200:
        runs = response.json()["workflow_runs"]
        for run in runs:
            if run["status"] == "in_progress" or run["status"] == "queued":
                return True
    return False

def trigger_workflow():
    response = requests.post(trigger_url, json=data, headers=headers)
    if response.status_code == 204:
        print("Workflow triggered successfully!")
    else:
        print(f"Failed to trigger workflow: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    while True:
        start_time = time.time()
        while time.time() - start_time < 5 * 60:  # Run for 5 minutes
            if not is_workflow_running():
                print("Workflow is not running. Triggering workflow...")
                trigger_workflow()
            else:
                print("Workflow is already running.")
            time.sleep(30)  # Check every 30 seconds

        print("Going to sleep for 6 hours...")
        time.sleep(6 * 60 * 60)  # Sleep for 6 hours
