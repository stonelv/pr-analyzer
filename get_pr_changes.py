import requests
from backend.app.core.config import settings

def get_pr_changes(pr_id):
    """Get changes for a specific PR"""
    print(f"Getting changes for PR ID: {pr_id}")
    
    # Check if the URL is a valid API endpoint
    if settings.GITLAB_BASE_URL and "/api/v4/" not in str(settings.GITLAB_BASE_URL):
        api_base_url = str(settings.GITLAB_BASE_URL).split('/')[0] + '//' + str(settings.GITLAB_BASE_URL).split('/')[2] + '/api/v4/'
    else:
        api_base_url = str(settings.GITLAB_BASE_URL)
    
    project_path = "MyCWTWebNet/OBT-PC-Code"
    api_url = f"{api_base_url}projects/{project_path.replace('/', '%2F')}/merge_requests/{pr_id}/changes"
    
    headers = {}
    if settings.GITLAB_TOKEN:
        headers["Private-Token"] = settings.GITLAB_TOKEN
    
    try:
        response = requests.get(api_url, headers=headers, verify=False)
        if response.status_code == 200:
            changes = response.json()
            print(f"Found {len(changes['changes'])} changed files")
            
            # Print some details about the changes
            for change in changes['changes']:
                print(f"- File: {change.get('new_path', change.get('old_path', 'unknown'))}")
                print(f"  Action: {change.get('action', 'unknown')}")
                if 'diff' in change:
                    print(f"  Diff: {change['diff'][:100]}...")
                # Print all keys for debugging
                print(f"  All keys: {list(change.keys())}")
            
            return changes
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    # Get changes for the first merged PR (ID: 578)
    get_pr_changes(578)