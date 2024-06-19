from abc import ABC, abstractmethod
from art import *
from termcolor import colored
from rich.console import Console;
from rich.panel import Panel;
from rich.markdown import Markdown;


class UIComponent(ABC):
    @abstractmethod
    def Draw():
        pass


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


class MarkdownComponent(UIComponent): 

    def __init__(self, text):
        self.text = text;

    
    def GenerateMarkdown(self):
        return Markdown(self.text);

    
    def Draw(self):
        console = Console();
        markdownObject = self.GenerateMarkdown();

        console.print(Panel(markdownObject, border_style="green", style="bold magenta"))


 












