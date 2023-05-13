import unittest
from unittest.mock import Mock, patch
import socket
import pickle
import json
import xml.etree.ElementTree as ET
from server import handle_received_data, server_program

class TestHandleReceivedData(unittest.TestCase):

    # Test handle_received_data function with the pickle format
    def test_handle_received_data_pickle(self):
        data = {'key': 'value'}
        serialized_data = pickle.dumps(data)
        result = handle_received_data(serialized_data, 'pickle')
        self.assertEqual(result, data)

    # Test handle_received_data function with the json format
    def test_handle_received_data_json(self):
        data = {'key': 'value'}
        serialized_data = json.dumps(data).encode()
        result = handle_received_data(serialized_data, 'json')
        self.assertEqual(result, data)

    # Test handle_received_data function with the xml format
    def test_handle_received_data_xml(self):
        data = {'key': 'value'}
        root = ET.Element('root')
        item = ET.SubElement(root, 'item')
        item.set('key', 'value')
        serialized_data = ET.tostring(root)
        result = handle_received_data(serialized_data, 'xml')
        self.assertEqual(result.tag, root.tag)

class TestServerProgram(unittest.TestCase):

    # Test server_program function using a mock socket
    @patch('socket.socket')
    def test_server_program(self, mock_socket):
        port = 11111

        # Set up the mock server socket
        mock_server_socket = Mock()
        mock_socket.return_value = mock_server_socket

        # Set up the mock connection and address
        mock_conn = Mock()
        mock_address = ('127.0.0.1', 54321)
        mock_server_socket.accept.return_value = (mock_conn, mock_address)

        # Set up the mock received data
        data = {'key': 'value'}
        format = 'json'
        serialized_data = f"{format};".encode() + json.dumps(data).encode()
        mock_conn.recv.return_value = serialized_data

        # Call the server_program function
        with self.assertRaises(SystemExit):
            server_program(port)

        # Assert server socket binding, listening and accepting connection
        mock_server_socket.bind.assert_called_once_with(('127.0.0.1', port))
        mock_server_socket.listen.assert_called_once_with(1)
        mock_server_socket.accept.assert_called_once()

        # Assert received data handling
        mock_conn.recv.assert_called_once_with(1024)

        # Assert connection close
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
