# GitHub Actions Activator Bot

An automated worker designed to bypass GitHub Actions' strict 6-hour execution limit. By monitoring target workflows and triggering fresh runs on a 6-hour interval schedule (00:00, 06:00, 12:00, and 18:00 UTC), this bot ensures your long-running tasks and services stay online almost continuously.

---

## Architecture & How It Works

This setup operates using **two separate repositories**:
1. **This Repository (Activator Bot):** Runs the Python monitoring script and sends API dispatches.
2. **Target Repository:** The repository hosting the actual workflow/bot you want to keep running continuously.

### Execution Flow
1. **Active Monitoring:** The bot queries the target repository to check if a workflow run is already `in_progress` or `queued`.
2. **Graceful Handover:** If an active job is detected, it waits for completion to allow continuous session rollover without overlapping resources.
3. **Automated Dispatch:** Once the current active session finishes or expires, the bot dispatches a new workflow run on your target repository via the GitHub REST API.

---

##  Required Repository Secrets / Environment Variables

To allow the activator bot to query and trigger workflows on your target repository, set up the following secrets under **Settings > Secrets and variables > Actions** in **this** repository:

| Secret Name | Description | Example Value |
| :--- | :--- | :--- |
| `GITHUB_TOKEN` | GitHub Personal Access Token  with `repo` and `workflow` permissions | `ghp_xxxxxxxxxxxx` |
| `REPO_OWNER` | GitHub username or organization owning the target repository | `Manasess896` |
| `REPO_NAME` | Name of the target repository you want to automate | `Test.main` |
| `WORKFLOW_ID` | Target workflow YAML filename or numeric workflow ID | `main.yml` |

---

##  Setup & Activation

> **Important Note:** To prevent this workflow from running automatically on the main repository, the schedule trigger in `.github/workflows/trigger.yml` is **disabled/commented out by default**. You must uncomment it in your copy to activate automated runs.

### 1. Activating the Bot Workflow
After cloning or forking this repository:

1. Open `.github/workflows/trigger.yml`.

2. Uncomment the `schedule` section so it looks like this:

```yaml
on:
  workflow_dispatch:

  schedule:
    - cron: '0 0 * * *'   # Runs at 00:00 UTC
    - cron: '0 6 * * *'   # Runs at 06:00 UTC
    - cron: '0 12 * * *'  # Runs at 12:00 UTC
    - cron: '0 18 * * *'  # Runs at 18:00 UTC