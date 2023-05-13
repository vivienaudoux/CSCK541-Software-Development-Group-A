import socket
import pickle
import json
import xml.etree.ElementTree as ET

# Function to serialize the dictionary data based on the pickling format
def serialize_data(data, format):
    if format == 'pickle':
        serialized_data = pickle.dumps(data)
    elif format == 'json':
        serialized_data = json.dumps(data).encode()
    elif format == 'xml':
        root = ET.Element('root')
        for key, value in data.items():
            item = ET.SubElement(root, 'item')
            item.set(key, str(value))
        serialized_data = ET.tostring(root)

    return serialized_data

# Main client program
def client_program(host, port, pickling_format):
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

    client_socket.close()

if __name__ == '__main__':
    client_program(host='127.0.0.1', port=11111, pickling_format='json')
    #Replace the pickling_format argument with the format: binary (pickle), json or XML)

