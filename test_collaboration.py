import requests
import json

# Test data
payload = {
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
            "author": "user1",
            "body": "Let me explain...",
            "created_at": "2023-01-01T11:00:00Z"
        },
        {
            "author": "user3",
            "body": "I think we should change this",
            "created_at": "2023-01-01T11:30:00Z"
        },
        {
            "author": "user1",
            "body": "I agree, let's update it",
            "created_at": "2023-01-01T12:00:00Z"
        }
    ]
}

# Send request
response = requests.post(
    "http://localhost:8080/api/analyze/collaboration",
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

# Print response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")