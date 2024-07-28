import socketserver
import http.server
import threading
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import socket

HOST, PORT = "0.0.0.0", 3000
SOCKET_SERVER_HOST, SOCKET_SERVER_PORT = "0.0.0.0", 5000


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.path = '/templates/index.html'
        elif parsed_path.path == '/message':
            self.path = '/templates/message.html'
        elif parsed_path.path.startswith('/static/'):
            self.path = self.path
        else:
            self.path = '/templates/error.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = parse_qs(post_data.decode('utf-8'))

            username = post_data.get('username', [''])[0]
            message = post_data.get('message', [''])[0]

            data = {
                "date": str(datetime.now()),
                "username": username,
                "message": message
            }

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))
                s.sendall(str(data).encode('utf-8'))

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(404)


def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server_address = (HOST, PORT)
    httpd = socketserver.TCPServer(server_address, CustomHandler)
    print(f"Serving HTTP on {HOST} port {PORT}...")
    httpd.serve_forever()


if __name__ == "__main__":
    threading.Thread(target=run_server).start()
