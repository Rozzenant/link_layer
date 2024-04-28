import requests
import json
from datetime import datetime
from network_ipv4 import get_wireless_ip

ip = get_wireless_ip()
url = f'http://{ip}:8000/code'


while True:
    payload = {
        "total_segments": "20",
        "segment_number": "3",
        "sender": "dan",
        "payload": "1000101001010011",
        "time": str(datetime.now())
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        if response.text.strip():
            print(f"Запрос к {url}")
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            print("Пустой ответ")
    else:
        print("Ошибка:", response.status_code)