from datetime import datetime
import requests

payload = {
    "total_segments": "1",
    "segment_number": "1",
    "sender": "dan",
    "payload": "Привет, мир!",
    "time": str(datetime.now())
}
response = requests.post("http://192.168.3.10:8080/transfer", json=payload)
print(response)