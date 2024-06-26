from modules.core.Ui.UiInterface import UIComponent


from art import *
from termcolor import colored

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

