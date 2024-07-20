import socket
from pymongo import MongoClient
import ast
SOCKET_SERVER = ('0.0.0.0', 5000)
MONGO_CONNECTION = 'mongodb://mongo:27017/'
client = MongoClient(MONGO_CONNECTION)
db = client['message_db']
collection = db['messages']
def save_to_mongo(data):
    collection.insert_one(data)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(SOCKET_SERVER)
    while True:
        data, addr = s.recvfrom(1024)
        message = ast.literal_eval(data.decode())
        save_to_mongo(message)
        print(f"Received and saved: {message}")
