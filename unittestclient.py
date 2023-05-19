import unittest
from unittest.mock import patch, Mock
import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet
from client import serialize_data, encrypt_file_content, read_file, client_program

class TestYourScript(unittest.TestCase):

    def test_serialize_data(self):
        data = {"test": 123}
        self.assertEqual(serialize_data(data, 'json'), json.dumps(data).encode())
        self.assertEqual(serialize_data(data, 'pickle'), pickle.dumps(data))
        xml_result = serialize_data(data, 'xml')
        root = ET.fromstring(xml_result)
        self.assertEqual(root[0].get('test'), str(data['test']))

    def test_encrypt_file_content(self):
        key = Fernet.generate_key()
        file_content = b'This is a test'
        f = Fernet(key)
        encrypted = encrypt_file_content(file_content, key)
        decrypted = f.decrypt(encrypted)
        self.assertEqual(file_content, decrypted)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'Test file content')
    def test_read_file(self, mock_file):
        self.assertEqual(read_file('fake_path'), b'Test file content')

    @patch('socket.socket')
    def test_client_program(self, MockSocket):
        instance = MockSocket.return_value
        host = '127.0.0.1'
        port = 11111
        pickling_format = 'json'
        file_path = 'file.txt'
        encrypt = True

        client_program(host, port, pickling_format, file_path, encrypt)
        instance.connect.assert_called_once_with((host, port))
        instance.sendall.assert_called()  # Asserting that sendall has been called, but not checking data


if __name__ == '__main__':
    unittest.main()

