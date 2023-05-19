import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet  # Importing Fernet for decryption

# Function to deserialize received data based on the pickling format
def handle_received_data(data, format):
    if format == 'pickle':
        deserialized_data = pickle.loads(data)
    elif format == 'json':
        deserialized_data = json.loads(data)
    elif format == 'xml':
        deserialized_data = ET.fromstring(data)

    return deserialized_data

# Function to decrypt the encrypted content using Fernet decryption
def decrypt_file_content(encrypted_content, key):
    f = Fernet(key)
    decrypted_content = f.decrypt(encrypted_content)
    return decrypted_content

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
    format, content = data.split(';', 1)
    content = content.encode()

    # Deserialize the received data
    received_data = handle_received_data(content, format)
    print("Received data:", received_data)

    while True:
        data = conn.recv(1024).decode()
        format, content = data.split(';', 1)
        content = content.encode()

        received_data = handle_received_data(content, format)

    # If the received data contains encrypted file content and key
    if isinstance(received_data, dict) and 'content' in received_data and 'key' in received_data:
        encrypted_content = received_data['content']
        encryption_key = received_data['key']

        # Decrypt the file content using the encryption key
        decrypted_content = decrypt_file_content(encrypted_content, encryption_key)

        # Save the decrypted content to a file
        with open('received_file.txt', 'wb') as file:
            file.write(decrypted_content)
            print("Encrypted file received and saved as 'received_file.txt'")
    else:
        # Save the received data to a file
        with open('received_data.txt', 'w') as file:
            file.write(str(received_data))
            print("Received data saved as 'received_data.txt'")

    conn.close()

if __name__ == '__main__':
    server_program(port=11111)
    #Arbitrary port number
