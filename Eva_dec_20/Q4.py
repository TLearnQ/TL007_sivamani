import requests
# Base API URL
TOKEN="mytoken"
headers = {
"Authorization": f"Bearer {TOKEN}",
 "Accept": "application/vnd.github+json"
}
url = "https://httpbin.org/delete"
response = requests.delete(url, headers=headers)
# Print results
print("Request URL:", url)
print("Status Code:", response.status_code)
if response.status_code == 200 or response.status_code == 204:
    print("Delete successful")
else:
    print("Delete failed:", response.text)