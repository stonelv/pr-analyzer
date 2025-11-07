import requests
from backend.app.core.config import settings

def test_gitlab_api():
    """Test GitLab API connection"""
    print(f"GitLab Base URL: {settings.GITLAB_BASE_URL}")
    print(f"GitLab Token: {settings.GITLAB_TOKEN}")
    
    # Check if the URL is a valid API endpoint
    # GitLab API endpoints typically start with /api/v4/
    if settings.GITLAB_BASE_URL and "/api/v4/" not in str(settings.GITLAB_BASE_URL):
        print("Warning: GITLAB_BASE_URL doesn't contain /api/v4/ - this might be a repository URL, not an API endpoint")
        print("Trying to extract API base URL...")
        # Extract the base URL (remove the repository path)
        api_base_url = str(settings.GITLAB_BASE_URL).split('/')[0] + '//' + str(settings.GITLAB_BASE_URL).split('/')[2] + '/api/v4/'
        print(f"Extracted API base URL: {api_base_url}")
    else:
        api_base_url = str(settings.GITLAB_BASE_URL)
    
    # Try to get project merge requests - check all states
    project_path = "MyCWTWebNet/OBT-PC-Code"
    
    # Check open MRs
    print("\n=== Checking open merge requests ===")
    api_url = f"{api_base_url}projects/{project_path.replace('/', '%2F')}/merge_requests?state=opened"
    check_merge_requests(api_url)
    
    # Check closed MRs
    print("\n=== Checking closed merge requests ===")
    api_url = f"{api_base_url}projects/{project_path.replace('/', '%2F')}/merge_requests?state=closed"
    check_merge_requests(api_url)
    
    # Check merged MRs
    print("\n=== Checking merged merge requests ===")
    api_url = f"{api_base_url}projects/{project_path.replace('/', '%2F')}/merge_requests?state=merged"
    check_merge_requests(api_url)

def check_merge_requests(api_url):
    """Check merge requests at the given API URL"""
    headers = {}
    if settings.GITLAB_TOKEN:
        headers["Private-Token"] = settings.GITLAB_TOKEN
    
    try:
        response = requests.get(api_url, headers=headers, verify=False)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            merge_requests = response.json()
            print(f"Found {len(merge_requests)} merge requests")
            if merge_requests:
                print(f"First MR: {merge_requests[0]['title']} (ID: {merge_requests[0]['iid']}, State: {merge_requests[0]['state']})")
            return merge_requests
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    test_gitlab_api()