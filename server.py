import socket
import pickle
import json
import xml.etree.ElementTree as ET

# Function to deserialize received data based on the pickling format
def handle_received_data(data, format):
    if format == 'pickle':
        deserialized_data = pickle.loads(data)
    elif format == 'json':
        deserialized_data = json.loads(data)
    elif format == 'xml':
        deserialized_data = ET.fromstring(data)

    return deserialized_data

# Main server program
def server_program(port):
    host = '127.0.0.1'
    #The host value '127.0.0.1' is set to "localhost" 
    #We will need to replace it with the actual IP address of the machine running the server code 
    # if we want to run this across different machines on a network.

    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server is listening on", host, ":", port)
    conn, address = server_socket.accept()
    print("Connection from:", address)

    # Receive serialized data from the client
    data = conn.recv(1024).decode()
    #1024 represents the maximum number of bytes that the server can receive at once from the client.
    # it's an arbitrary choice and can be modified. 
    format, content = data.split(';', 1)
    content = content.encode()

    # Deserialize the received data
    received_data = handle_received_data(content, format)
    print("Received data:", received_data)

    conn.close()

if __name__ == '__main__':
    server_program(port=11111)
    #Arbitrary port number
