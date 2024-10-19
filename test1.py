import requests
import json

# Test authentication via access token
endpoint = "http://127.0.0.1:8000/water/user/parameters/list/"
endpost = "http://127.0.0.1:8000/water/user/parameters/add/"

access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5OTEzNzE1LCJpYXQiOjE3MTc5MzM3MTUsImp0aSI6IjhkOTMzZTI0YzQ4NzRhN2FiZjU1NjM2MzIzZmNkMjM5IiwidXNlcl9pZCI6M30.9RU1PfymyroHWu4zCIyvs0UUoAelc06uPizohUnUHRk"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer_inera {access_token}"  
}

data_list = [
    {
        "ph": "14",
        "oxygen": "23",
        "turbidity": "34",
        "temperature": "23",
        "user":3,
        "harvesting_time": "2024-06-09T10:00:00Z"
    },
    {
        "ph": "7",
        "oxygen": "15",
        "turbidity": "20",
        "temperature": "18",
        "user":3,
        "harvesting_time": "2024-06-10T11:00:00Z"
    },
    {
        "ph": "8",
        "oxygen": "18",
        "turbidity": "25",
        "temperature": "20",
        "user":3,
        "harvesting_time": "2024-06-11T12:00:00Z"
    }
    # Add more data dictionaries as needed
]

for data in data_list:
    try:
        resp = requests.post(endpost, data=json.dumps(data), headers=headers)
        resp.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        print(f"POST Response: {resp.json()}")
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")

try:
    get_exo = requests.get(endpoint, headers=headers)
    get_exo.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    print(f"GET Response: {get_exo.json()}")
except requests.exceptions.RequestException as e:
    print(f"GET request failed: {e}")
