import asyncio
import datetime
import socket
from pathlib import Path
from urllib.parse import parse_qs
BASE_DIR = Path()
SOCKET_SERVER = ('localhost', 5000)
def send_to_socket_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(data.encode(), SOCKET_SERVER)
async def handle_request(reader, writer):
    request = await reader.read(1024)
    request = request.decode()
    
    method, path, _ = request.split('\n')[0].split()
    
    if method == 'GET':
        if path == '/':
            filename = BASE_DIR / 'templates' / 'index.html'
        elif path == '/message':
            filename = BASE_DIR / 'templates' / 'message.html'
        elif path.startswith('/static/'):
            filename = BASE_DIR / path[1:]
        else:
            filename = BASE_DIR / 'templates' / 'error.html'
            
        if filename.exists():
            with open(filename, 'rb') as f:
                content = f.read()
            writer.write(b'HTTP/1.1 200 OK\n\n' + content)
        else:
            with open(BASE_DIR / 'templates' / 'error.html', 'rb') as f:
                content = f.read()
            writer.write(b'HTTP/1.1 404 Not Found\n\n' + content)
    
    elif method == 'POST' and path == '/message':
        content_length = int(request.split('Content-Length: ')[1].split('\n')[0])
        body = await reader.read(content_length)
        data = parse_qs(body.decode())
        
        message = {
            'date': datetime.datetime.now().isoformat(),
            'username': data['username'][0],
            'message': data['message'][0]
        }
        
        send_to_socket_server(str(message))
        
        writer.write(b'HTTP/1.1 302 Found\nLocation: /\n\n')
    
    await writer.drain()
    writer.close()
async def main():
    server = await asyncio.start_server(handle_request, '0.0.0.0', 3000)
    async with server:
        await server.serve_forever()
if __name__ == '__main__':
    asyncio.run(main())
