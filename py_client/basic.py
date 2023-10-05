import requests

endpoint = "http://localhost:8000/api/"

response = requests.post(endpoint, params={"id": 1},
                         json={
                             "title": "Test Post Title Fuction Test.",
                             "content": "This is Test Post Request Content",
                             "price": 327,
                         })

print(response.text)
