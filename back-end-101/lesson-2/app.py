import requests
import pytorch

response = requests.get('https://api.github.com')
print(f"Статус код ответа: {response.status_code}")