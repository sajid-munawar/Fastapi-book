import requests
import httpx

params = {"who": "Mom"}
r = requests.get("http://localhost:8000/hi", params=params)
print(r.json())

# req=requests.get('http://localhost:8000/hi')
# print(req.json())

# r = httpx.get("http://localhost:8000/hi")
# print(r.json())
