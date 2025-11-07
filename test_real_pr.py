import requests
import json
from backend.app.core.config import settings

def get_api_base_url():
    """Get the GitLab API base URL"""
    if settings.GITLAB_BASE_URL and "/api/v4/" not in str(settings.GITLAB_BASE_URL):
        return str(settings.GITLAB_BASE_URL).split('/')[0] + '//' + str(settings.GITLAB_BASE_URL).split('/')[2] + '/api/v4/'
    else:
        return str(settings.GITLAB_BASE_URL)

def get_gitlab_headers():
    """Get GitLab API headers with authentication"""
    headers = {}
    if settings.GITLAB_TOKEN:
        headers["Private-Token"] = settings.GITLAB_TOKEN
    return headers

def get_real_pr_data():
    """Get real PR data from GitLab API"""
    api_base_url = get_api_base_url()
    project_path = "MyCWTWebNet/OBT-PC-Code"
    
    # Get the first merged PR
    api_url = f"{api_base_url}projects/{project_path.replace('/', '%2F')}/merge_requests?state=merged&per_page=1"
    headers = get_gitlab_headers()
    
    try:
        response = requests.get(api_url, headers=headers, verify=False)
        if response.status_code == 200:
            prs = response.json()
            if prs:
                pr = prs[0]
                print(f"Found PR: {pr['title']} (ID: {pr['iid']})")
                
                # Get PR changes
                changes_url = f"{api_base_url}projects/{project_path.replace('/', '%2F')}/merge_requests/{pr['iid']}/changes"
                changes_response = requests.get(changes_url, headers=headers, verify=False)
                if changes_response.status_code == 200:
                    pr['changes'] = changes_response.json()['changes']
                    return pr
        return None
    except Exception as e:
        print(f"Error getting PR data: {e}")
        return None

def test_api_endpoints(pr_data):
    """Test all API endpoints with real PR data"""
    print("\n=== Testing API endpoints with real PR data ===")
    
    # Test health check
    print("\n1. Testing health check endpoint...")
    response = requests.get("http://localhost:8080/api/healthz")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    
    # Test code complexity with a real file from the PR
    print("\n2. Testing code complexity endpoint...")
    if pr_data and 'changes' in pr_data:
        for change in pr_data['changes']:
            if 'diff' in change and change['diff']:
                # Extract some code from the diff
                diff_lines = change['diff'].split('\n')
                # Find added lines (starting with '+')
                added_code = '\n'.join([line[1:] for line in diff_lines if line.startswith('+') and not line.startswith('+++')])
                if added_code:
                    # Test with the added code
                    payload = {
                        "code": added_code,
                        "language": "csharp"  # Assuming C# since it's .aspx.cs files
                    }
                    response = requests.post("http://localhost:8080/api/analyze/complexity", json=payload)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   Complexity: {result['result']['cyclomatic_complexity']}")
                        print(f"   Halstead Volume: {result['result']['halstead_volume']}")
                    break
    
    # Test code duplication with a real file from the PR
    print("\n3. Testing code duplication endpoint...")
    if pr_data and 'changes' in pr_data:
        for change in pr_data['changes']:
            if 'diff' in change and change['diff']:
                # Extract some code from the diff
                diff_lines = change['diff'].split('\n')
                # Find added lines (starting with '+')
                added_code = '\n'.join([line[1:] for line in diff_lines if line.startswith('+') and not line.startswith('+++')])
                if added_code:
                    # Test with the added code
                    payload = {
                        "code": added_code,
                        "language": "csharp",
                        "min_lines": 2
                    }
                    response = requests.post("http://localhost:8080/api/analyze/code-duplication", json=payload)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   Duplicate Lines: {result['result']['total_duplicate_lines']}")
                        print(f"   Duplication Ratio: {result['result']['duplication_ratio']}")
                    break
    
    # Test security scan with a real file from the PR
    print("\n4. Testing security scan endpoint...")
    if pr_data and 'changes' in pr_data:
        for change in pr_data['changes']:
            if 'diff' in change and change['diff']:
                # Extract some code from the diff
                diff_lines = change['diff'].split('\n')
                # Find added lines (starting with '+')
                added_code = '\n'.join([line[1:] for line in diff_lines if line.startswith('+') and not line.startswith('+++')])
                if added_code:
                    # Test with the added code
                    payload = {
                        "code": added_code,
                        "language": "csharp"
                    }
                    response = requests.post("http://localhost:8080/api/analyze/security-scan", json=payload)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   Vulnerabilities: {result['result']['total_vulnerabilities']}")
                    break
    
    print("\n=== All API tests completed ===")

if __name__ == "__main__":
    print("=== Testing PR Analyzer with real GitLab data ===")
    
    # Get real PR data
    pr_data = get_real_pr_data()
    if pr_data:
        print(f"\nPR Details:")
        print(f"Title: {pr_data['title']}")
        print(f"Author: {pr_data['author']['name']}")
        print(f"Created: {pr_data['created_at']}")
        print(f"Merged: {pr_data['merged_at']}")
        print(f"Changed Files: {len(pr_data['changes'])}")
        
        # Test API endpoints
        test_api_endpoints(pr_data)
    else:
        print("Failed to get real PR data from GitLab API")