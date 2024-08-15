import requests
import time
import os
import signal
import sys

# Fetch environment variables
GITHUB_TOKEN = os.getenv('TOKEN')
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

# Function to handle the timeout
def timeout_handler(signum, frame):
    print("Operation timed out")
    sys.exit(1)  # Exit with error code 1

# Set the signal handler and a timeout of 5 minutes (300 seconds)
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(300)  # Timeout after 300 seconds

def is_workflow_running():
    try:
        response = requests.get(workflow_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        runs = response.json().get("workflow_runs", [])
        for run in runs:
            if run["status"] in ["in_progress", "queued"]:
                print(f"Workflow run detected: {run['id']} with status: {run['status']}")
                return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking workflow status: {e}")
        return False

def trigger_workflow():
    try:
        response = requests.post(trigger_url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        if response.status_code == 204:
            print("Workflow triggered successfully!")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error triggering workflow: {e}")

if __name__ == "__main__":
    workflow_triggered = False
    start_time = time.time()

    while time.time() - start_time < 5 * 60:  # Run for 5 minutes
        if not is_workflow_running():
            print("Workflow is not running. Attempting to trigger...")
            trigger_workflow()
            workflow_triggered = True
            time.sleep(30)  # Wait before checking again
        else:
            print("Workflow is already running.")
            workflow_triggered = True
            time.sleep(30)  # Wait before checking again

    if not workflow_triggered:
        print("No action was taken during this cycle.")
    
    print("Going to sleep for 6 hours...")
    time.sleep(6 * 60 * 60)  # Sleep for 6 hours

    # Check if the workflow was triggered successfully
    if workflow_triggered:
        print("Workflow triggered successfully!")
        sys.exit(0)  # Exit with code 0 for success
    else:
        print("Failed to trigger workflow.")
        sys.exit(1)  # Exit with code 1 for failure
