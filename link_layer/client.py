import random
import requests
import json
from datetime import datetime
from network_ipv4 import get_wireless_ip


def generate_random_binary():
    while True:
        yield str(random.randint(0, 1))


ip = get_wireless_ip()
url = f'http://{ip}:8000/code'


while True:
    random_gen = generate_random_binary()
    message = ''.join([next(random_gen) for _ in range(random.randint(1, 1000))])
    payload = {
        "payload": f"{message}",
        "total_segments": "1",
        "segment_number": "1",
        "sender": "dan",
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