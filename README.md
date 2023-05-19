# CSCK541-Software-Development-Group-A

The code consists of two Python scripts: client.py and server.py. These scripts implement a client-server communication using sockets, allowing the client to send data to the server. The data can be serialized in different formats (pickle, JSON, or XML) and optionally encrypted using Fernet encryption.

client.py
The client.py script contains the following functions:
1) serialize_data(data, format): Serializes the provided dictionary data based on the specified format (pickle, JSON, or XML).
2) encrypt_file_content(file_content, key): Encrypts the provided file content using Fernet encryption.
3) read_file(file_path): Reads the content of a file specified by the file path.
4) client_program(host, port, pickling_format, file_path=None, encrypt=False): The main client program that establishes a connection with the server and sends data. It serializes the dictionary data, sends it to the server, and optionally sends the content of a file. If encryption is enabled, it encrypts the file content using Fernet encryption.

server.py 
The server.py script contains the following functions:
1) handle_received_data(data, format): Deserializes the received data based on the specified format (pickle, JSON, or XML).
2) decrypt_file_content(encrypted_content, key): Decrypts the provided encrypted content using Fernet decryption.
3) server_program(port): The main server program that listens for incoming connections from clients. It receives data from the client, handles the received data, and saves it to a file. If the received data includes encrypted file content, it decrypts it using the provided key.

Usage
To use the code, follow these steps:
1) Ensure you have Python 3 installed on your machine.
2) Install the required dependencies by running the following command in your terminal: pip install cryptography
3) Save the client.py and server.py files in your desired directory.
4) Open two separate terminal windows or tabs. One will be used to run the server, and the other will run the client.
5) In the server terminal, navigate to the directory where the server.py file is located and run the following command: python server.py
This will start the server and make it listen for incoming connections on the default IP address 127.0.0.1 and port 11111.
6) In the client terminal, navigate to the directory where the client.py file is located and open the file in a text editor.
Modify the host, port, pickling_format, file_path, and encrypt variables in the client.py file according to your needs. These variables specify the server's IP address and port, the serialization format, the file path (if applicable), and whether encryption is enabled or not. Save the client.py file after making the necessary modifications.
7) In the client terminal, run the following command to execute the client program: python client.py
This will establish a connection with the server and send the data. The server will receive the data, handle it, and save it to a file (received_file.txt for encrypted content or received_data.txt for non-encrypted content).

Testing
The code includes unit tests to verify the functionality of the implemented functions. The tests are defined in the files test_client.py and test_server.py.
To run the tests, follow these steps:
1) Open a terminal and navigate to the directory where the code files are located.
2) Run the following command to execute the client tests: python -m unittest test_client.py
3) Run the following command to execute the server tests: python -m unittest test_server.py
The tests will run, and the output will indicate whether all the tests passed or if there were any failures.
