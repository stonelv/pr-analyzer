import requests

url = 'https://gitlab.mycwt.com.cn/MyCWTWebNet/OBT-PC-Code.git'

print(f"Checking GitLab URL: {url}")

try:
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response content (first 200 chars): {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")