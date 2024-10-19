import requests
import json

# Test authentication via APIKey
endpoint = "http://192.168.18.58:8000/water/iot/parameters/list/"
endpost = "http://192.168.18.58:8000/water/iot/parameters/add/"

key = "Jv4EXtyv.BAbCJN5FK7wwaponCTyRkQPKnkPFE2fg"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {key}"
}

data = {
    "ph": "5.8",
    "temperature": "22",
    "harvesting_time": "2024-06-09T10:00:00Z"  # Example datetime, adjust as needed
}

try:
    for i in range(15):
        data = {
    "ph": f"{5.8 + 2*i}",
    "temperature": f"{22 + 2*i}",
    "harvesting_time": "2024-06-09T10:00:00Z"  # Example datetime, adjust as needed
    }
        resp = requests.post(endpost, data=json.dumps(data), headers=headers)
        resp.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        print(f"POST Response: {resp.json()}")
except requests.exceptions.RequestException as e:
    print(f"POST request failed: {e}")