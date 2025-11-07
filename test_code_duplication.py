import requests
import json

# Test data
payload = {
    "code": "def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef add(a, b):\n    return a + b",
    "language": "python",
    "min_lines": 2
}

# Send request
response = requests.post(
    "http://localhost:8080/api/analyze/code-duplication",
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

# Print response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")