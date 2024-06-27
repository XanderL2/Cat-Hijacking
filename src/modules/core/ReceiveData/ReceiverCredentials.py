import socket, json, re;
from abc import ABC, abstractmethod;

from modules.core.ReceiveData.interface.packageReceiver  import PackageReceiver



class ReceiverCredentials(PackageReceiver):

    
    def __init__(self, ip, port): 
        self._port = port;
        self._ip = ip;
        

    def ReceiverPackage(self):

   
        # Create Socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Establish connection 
        serverAddress = (self._ip, self._port)

        try:
            clientSocket.connect(serverAddress)

        except socket.error as e:
            raise ConnectionError(f"Failed to connect to {serverAddress}") from e

        try:
            data = ""
            while True:
                chunk = clientSocket.recv(4096).decode("utf-8")
                if not chunk:
                    break
                data += chunk;


            return json.loads(data);

        except json.JSONDecodeError as e:
            raise ValueError("Error deserializing JSON") from e
        
        finally:
            clientSocket.close()

    
    






