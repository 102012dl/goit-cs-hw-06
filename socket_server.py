import socket
import pymongo
from datetime import datetime

MONGO_URI = "mongodb://mongo:27017/"
DB_NAME = "messages_db"
COLLECTION_NAME = "messages"

HOST, PORT = "0.0.0.0", 5000

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    data = eval(request.decode('utf-8'))
    collection.insert_one(data)
    client_socket.close()

def run_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Socket server listening on {HOST} port {PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        handle_client_connection(client_socket)

if __name__ == "__main__":
    run_socket_server()
