from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
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
            print(data)
            # encoded_segment, remainder = encoding_hamming_code_7_4(''.join(f"{char:08b}" for char in data[
            #     'payload'].encode('utf-8')))
            encoded_segment, remainder = encoding_hamming_code_7_4(data['payload'])
            error_segment = corrupt_hamming_code(encoded_segment)
            decoded_error_segment = decoding_hamming_code_7_4(error_segment, remainder)

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

            response = json.dumps(response_data)
            self.wfile.write(response.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('404')


def run(ipv4, server_class=HTTPServer, handler_class=HttpHandler):
    server_address = (ipv4, 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    ip = get_wireless_ip()
    print(f'Сервер запущен по адресу {ip}:8000...')
    run(ip)
    print('Сервер выключен')
