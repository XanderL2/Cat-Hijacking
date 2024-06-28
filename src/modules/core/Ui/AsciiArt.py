from modules.core.Ui.interface.UiInterface import UIComponent

from art import *
from termcolor import colored
from colorama import Fore, Style


class AsciiArt(UIComponent):

    def __init__(self, text, font, color): 
        self.text = text;
        self.font = font;
        self.color =  color;

    def GenerateAscii(self):
        asciiText= text2art(self.text, font = self.font)
        return colored(asciiText, self.color)


    def Draw(self):
        print(self.GenerateAscii());


    def Warn(self, text):
        return print(Fore.YELLOW + "[!]\t" + text + "  󱆃" + Fore.RESET);

    def Info(self, text):
        return print(Fore.BLUE+ "[*]\t" + text + "  " + Fore.RESET);

    def Success(self, text):
        return print(Fore.GREEN+ "[+]\t" + text + "  󰈸" + Fore.RESET);


    def Failure(self, text):
        return print(Fore.RED + "[-]\t" + text + "  " + Fore.RESET);




    
    