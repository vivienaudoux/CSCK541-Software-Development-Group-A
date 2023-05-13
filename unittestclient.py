import socket
import unittest
from unittest.mock import Mock, patch
import pickle
import json
import xml.etree.ElementTree as ET
from client import serialize_data, client_program

# Create a test class for the serialize_data function
class TestSerializeData(unittest.TestCase):

    # Test serialize_data function with the pickle format
    def test_serialize_data_pickle(self):
        data = {'key': 'value'}
        result = serialize_data(data, 'pickle')
        self.assertEqual(result, pickle.dumps(data))

    # Test serialize_data function with the json format
    def test_serialize_data_json(self):
        data = {'key': 'value'}
        result = serialize_data(data, 'json')
        self.assertEqual(result, json.dumps(data).encode())

    # Test serialize_data function with the xml format
    def test_serialize_data_xml(self):
        data = {'key': 'value'}
        result = serialize_data(data, 'xml')
        root = ET.Element('root')
        item = ET.SubElement(root, 'item')
        item.set('key', 'value')
        expected_result = ET.tostring(root)
        self.assertEqual(result, expected_result)

# Create a test class for the client_program function
class TestClientProgram(unittest.TestCase):

    # Test client_program function using a mock socket
    @patch('socket.socket')
    def test_client_program(self, mock_socket):
        host = '127.0.0.1'
        port = 11111
        pickling_format = 'json'

        # Set up the mock socket
        mock_socket_instance = Mock()
        mock_socket.return_value = mock_socket_instance

        # Call the client_program function
        client_program(host, port, pickling_format)

        # Assert socket connection
        mock_socket_instance.connect.assert_called_once_with((host, port))

        # Assert serialized data sent to the server
        dictionary_data = {'Student1': 'Muhammad Abba Shariff', 'Student2': 'Vivien Audoux', 'Student3': 'Moran Ron', 'Student4': 'Sin Yi Cynthia Wong', 'Student5': 'Man Sze Wong'}
        serialized_data = serialize_data(dictionary_data, pickling_format)
        data_to_send = f"{pickling_format};".encode() + serialized_data
        mock_socket_instance.sendall.assert_called_once_with(data_to_send)

        # Assert socket close
        mock_socket_instance.close.assert_called_once()

# Run the tests using the unittest module
if __name__ == '__main__':
    unittest.main()
