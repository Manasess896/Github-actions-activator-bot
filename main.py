import os
import sys
import time
import requests

#fetch environment variables
GITHUB_TOKEN = os.getenv('TOKEN') or os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')
WORKFLOW_ID = os.getenv('WORKFLOW_ID')
REF = os.getenv('REF', 'main')


missing_vars = [
    name for name, val in [
        ('TOKEN', GITHUB_TOKEN),
        ('REPO_OWNER', REPO_OWNER),
        ('REPO_NAME', REPO_NAME),
        ('WORKFLOW_ID', WORKFLOW_ID),
    ] if not val
]

if missing_vars:
    sys.exit(f"Error: Missing required environment variables: {', '.join(missing_vars)}")



BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_ID}"
RUNS_URL = f"{BASE_URL}/runs"
DISPATCH_URL = f"{BASE_URL}/dispatches"


session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
})

def is_workflow_running(ref: str = REF) -> bool:
    """Checks if any run for the workflow is queued or in progress on the target branch."""
    try:
        response = session.get(RUNS_URL, params={"branch": ref})
        response.raise_for_status()
        
        runs = response.json().get("workflow_runs", [])
        active_statuses = {"in_progress", "queued", "waiting", "requested"}
        
        for run in runs:
            if run.get("status") in active_statuses:
                print(f"Active run detected (ID: {run['id']}, Status: {run['status']})")
                return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking workflow status: {e}")
        return False

def trigger_workflow(ref: str = REF) -> bool:
    """Dispatches a new workflow run. Returns True on success, False on failure."""
    try:
        response = session.post(DISPATCH_URL, json={"ref": ref})
        response.raise_for_status()
        
        if response.status_code == 204:
            print(f"Workflow dispatched successfully on '{ref}'!")
            return True
        
        print(f"Unexpected API response ({response.status_code}): {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error triggering workflow: {e}")
        return False

def main():
    timeout = 30 * 60  #30 minutes
    poll_interval = 15  #15 seconds 
    start_time = time.time()

    print(f"Monitoring workflow for {REPO_OWNER}/{REPO_NAME} (Branch: {REF})...")

    while time.time() - start_time < timeout:
        if not is_workflow_running(REF):
            print("No active workflow detected. Attempting dispatch...")
            if trigger_workflow(REF):
                sys.exit(0)
            print("Dispatch attempt failed. Retrying on next check...")
        else:
            print(f"Workflow is active. Retrying in {poll_interval} seconds...")
            
        time.sleep(poll_interval)

    print("Error: Timed out waiting to trigger workflow.")
    sys.exit(1)

if __name__ == "__main__":
    main()