from datetime import datetime
import requests

payload = {
    "total_segments": "20",
    "segment_number": "3",
    "sender": "dan",
    "payload": "Двигает все, что не движется",
    "time": str(datetime.now())
}
response = requests.post("http://192.168.3.10:8080/transfer", json=payload)
print(response)