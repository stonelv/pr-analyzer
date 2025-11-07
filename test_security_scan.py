import requests
import json

# Test data
payload = {
    "code": "import os\npassword = input('Enter password: ')\nos.system(f'echo {password}')",
    "language": "python"
}

# Send request
response = requests.post(
    "http://localhost:8080/api/analyze/security-scan",
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

# Print response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")