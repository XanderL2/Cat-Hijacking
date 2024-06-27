import socket, json
from abc import ABC, abstractmethod;

from src.modules.core.ReceiveData.interface.packageReceiver  import PackageReceiver



class ReceiverCredentials(PackageReceiver):

    
    def __init__(self, port, ip = ""): 
        self._port = port;
        self._ip = ip;
        

    def ReceivePackage(self):

   
        # Create Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Establish connection 
        server_address = (self._ip, self._port)
        try:
            client_socket.connect(server_address)

        except socket.error as e:
            raise ConnectionError(f"Failed to connect to {server_address}") from e

        try:
            data = ""
            while True:
                chunk = client_socket.recv(4096).decode("utf-8")
                if not chunk:
                    break
                data += chunk;

            return json.loads(data)

        except json.JSONDecodeError as e:
            raise ValueError("Error deserializing JSON") from e
        
        finally:
            client_socket.close()

    
    






