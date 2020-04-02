import requests
res = requests.get("http://127.0.0.1:5000/api/search", params={"key": "SlY6kcXclNU5WAwmYVMdKw", "isbns": "9781632168146"})
print(res.json())