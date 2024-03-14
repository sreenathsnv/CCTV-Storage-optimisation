import requests

url = "http://127.0.0.1:8000/api/test"



res = requests.get(url)

print(res.json())