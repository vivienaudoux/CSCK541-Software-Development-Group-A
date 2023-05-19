import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet  # Importing Fernet for encryption

# Function to serialize the dictionary data based on the pickling format
def serialize_data(data, format):
    if format == 'pickle':
        serialized_data = pickle.dumps(data)
    elif format == 'json':
        if isinstance(data, bytes):
            data = data.hex()
        serialized_data = json.dumps(data).encode()
    elif format == 'xml':
        root = ET.Element('root')
        for key, value in data.items():
            item = ET.SubElement(root, 'item')
            item.set(key, str(value))
        serialized_data = ET.tostring(root)

    return serialized_data

# Function to encrypt the file content using Fernet encryption
def encrypt_file_content(file_content, key):
    f = Fernet(key)
    encrypted_content = f.encrypt(file_content)
    return encrypted_content

# Function to read the file content
def read_file(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return file_content

# Main client program
def client_program(host, port, pickling_format, file_path=None, encrypt=False):
    # Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Create and populate a dictionary
    dictionary_data = {'Student1': 'Muhammad Abba Shariff', 'Student2': 'Vivien Audoux', 'Student4': 'Sin Yi Cynthia Wong', 'Student5': 'Man Sze Wong'}

    # Serialize the dictionary data
    serialized_data = serialize_data(dictionary_data, pickling_format)

    # Send the serialized data to the server
    data_to_send = f"{pickling_format};".encode() + serialized_data
    client_socket.sendall(data_to_send)

    # If file_path is provided, read the file content and send it to the server
    if file_path:
        file_content = read_file(file_path)

        # Encrypt the file content if encrypt flag is set
        if encrypt:
            key = Fernet.generate_key()
            encrypted_content = encrypt_file_content(file_content, key)

            # Convert the key to hexadecimal for serialization
            key_hex = key.hex()

            encrypted_data = {'content': encrypted_content.hex(), 'key': key_hex}
            serialized_encrypted_data = serialize_data(encrypted_data, pickling_format)

            # Send the encrypted file content
            data_to_send = f"{pickling_format};".encode() + serialized_encrypted_data
            client_socket.sendall(data_to_send)
        else:
            # Send the file content as it is
            client_socket.sendall(file_content)

    client_socket.close()

if __name__ == '__main__':
    # Specify the host, port, pickling_format, file_path, and encrypt flag
    host = '127.0.0.1'
    port = 11111
    pickling_format = 'json'
    file_path = 'file.txt'  # Path to the file to be sent
    encrypt = True  # Set to True if encryption is required, False otherwise

    client_program(host, port, pickling_format, file_path, encrypt)
