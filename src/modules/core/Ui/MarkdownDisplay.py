from modules.core.Ui.interface.UiInterface import UIComponent

from rich.console import Console;
from rich.panel import Panel;
from rich.markdown import Markdown;




class MarkdownComponent(UIComponent): 

    def __init__(self, text):
        self.text = text;

    
    def __GenerateMarkdown(self):
        return Markdown(self.text);

    
    def Draw(self):
        console = Console();
        markdownObject = self.__GenerateMarkdown();

        console.print(Panel(markdownObject, border_style="green", style="bold magenta"))


 












