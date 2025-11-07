import requests
import json

def test_endpoint(name, url, method="GET", data=None):
    """Test an API endpoint and print the result"""
    print(f"\n=== Testing {name} ===")
    print(f"URL: {url}")
    print(f"Method: {method}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data) if data else None
            )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

# Test all endpoints
print("Testing all PR Analyzer API endpoints...")

# Health check
test_endpoint("Health Check", "http://localhost:8080/api/healthz")

# Code complexity
test_endpoint(
    "Code Complexity",
    "http://localhost:8080/api/analyze/complexity",
    method="POST",
    data={
        "code": "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
        "language": "python"
    }
)

# Test coverage
test_endpoint(
    "Test Coverage",
    "http://localhost:8080/api/analyze/test-coverage",
    method="POST",
    data={
        "baseline_coverage": {"total": 80.0, "files": {"test1.py": {"coverage": 90.0, "lines": {"1": True, "2": True, "3": True}}}},
        "pr_coverage": {"total": 75.0, "files": {"test1.py": {"coverage": 85.0, "lines": {"1": True, "2": False, "3": True, "4": False}}}}
    }
)

# Dependency changes
test_endpoint(
    "Dependency Changes",
    "http://localhost:8080/api/analyze/dependency-changes",
    method="POST",
    data={
        "baseline_deps": {"requests": "2.28.0", "django": "3.2.15"},
        "pr_deps": {"requests": "2.29.0", "django": "4.1.0", "newpackage": "1.0.0"}
    }
)

# Security scan
test_endpoint(
    "Security Scan",
    "http://localhost:8080/api/analyze/security-scan",
    method="POST",
    data={
        "code": "import os\npassword = input('Enter password: ')\nos.system(f'echo {password}')",
        "language": "python"
    }
)

# Code duplication
test_endpoint(
    "Code Duplication",
    "http://localhost:8080/api/analyze/code-duplication",
    method="POST",
    data={
        "code": "def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef add(a, b):\n    return a + b",
        "language": "python",
        "min_lines": 2
    }
)

# Collaboration efficiency
test_endpoint(
    "Collaboration Efficiency",
    "http://localhost:8080/api/analyze/collaboration",
    method="POST",
    data={
        "comments": [
            {
                "author": "user1",
                "body": "This looks good!",
                "created_at": "2023-01-01T10:00:00Z"
            },
            {
                "author": "user2",
                "body": "I have a question about this part",
                "created_at": "2023-01-01T10:30:00Z"
            },
            {
                "author": "user3",
                "body": "I think we should change this",
                "created_at": "2023-01-01T11:30:00Z"
            }
        ]
    }
)

print("\n=== All tests completed ===")