import requests
import os
import json

api_key = os.getenv("NYT_API_KEY")
if not api_key:
    raise ValueError("NYT_API_KEY environment variable is not set.")

url = f"https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json"
params={
    "api-key": api_key
}

response = requests.get(url,params=params)

if response.status_code == 200:
    data = response.json()
    print("Datos recibidos:")
    print(data)
else:
    print(f'Error: {response.status_code}')
    print(response.text)

