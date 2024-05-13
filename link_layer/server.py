from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

import requests

from network_ipv4 import get_wireless_ip
from HammingFunc import *
import json


class HttpHandler(BaseHTTPRequestHandler):
    """Обработчик POST"""

    def do_POST(self):
        print(self.path)
        if self.path == '/code':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            # print(data)
            # encoded_segment, remainder = encoding_hamming_code_7_4(''.join(f"{char:08b}" for char in data[
            #     'payload'].encode('utf-8')))
            encoded_segment, remainder = encoding_hamming_code_7_4(data['payload'])
            error_segment = corrupt_hamming_code(encoded_segment)
            decoded_error_segment = decoding_hamming_code_7_4(error_segment, remainder)

            if data['payload'] != decoded_error_segment:
                if decoded_error_segment:
                    raise ValueError("Несовпадение")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # decoded_error_segment = bytearray(int(decoded_error_segment[i:i + 8], 2) for i in range(0, len(decoded_error_segment), 8)).decode('utf-8')

            response_data = {
                "payload": decoded_error_segment,
                "total_segments": data['total_segments'],
                "segment_number": data['segment_number'],
                "sender": data['sender'],
                "time": data['time']
            }

            # data = requests.post("http://192.168.3.10:8000/transfer/", json=response_data)
            # print(data)

            response = requests.post("http://192.168.52.44:8000/transfer/", json=response_data)
            if response.status_code == 200:
                # print(f"Запрос к http://192.168.52.44:8000/transfer/ - Status 200\n")

                if response.text.strip():
                    print(json.dumps(response.json(), indent=4, ensure_ascii=False))

            response = json.dumps(response_data)
            self.wfile.write(response.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()


def run(ipv4, server_class=HTTPServer, handler_class=HttpHandler):
    server_address = (ipv4, 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    try:
        ip = get_wireless_ip()
    except ImportError:
        ip = "127.0.0.1"
    print(f'Сервер запущен по адресу {ip}:8000...\n')
    run(ip)
    print('Сервер выключен')
