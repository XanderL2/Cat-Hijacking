from modules.core.Ui.AsciiArt import AsciiArt
from modules.core.Ui.MarkdownDisplay import MarkdownComponent

import argparse, re, sys





def main():

    # Parameters with console
    # parser = argparse.ArgumentParser(description='Session Hijacking Script');

    # parser.add_argument("-ip", "--VictimIP", required=True, type=str, help="Victim's IP to receive the data");
    # parser.add_argument("-p", "--ConnectionPort", required=False, type=int, default=8000, help="Connection port to receive cookies");


    # args = parser.parse_args();
    # ip = args.VictimIP;
    # port = args.ConnectionPort; 






    # if (not re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)):
    #     print("Error! Invalid IP")
    #     sys.exit()



    # Drawing cover
    asciiRenderer = AsciiArt("Py Hijacking ", "sblood", "magenta");

    ip = "192.168.1.100"
    port = "8080"

    
    with open("./assets/cover.md", "r") as file:
        markdownData = file.read().format(asciiArt=asciiRenderer.GenerateAscii(), ip=ip, port=port);



    markdownRender = MarkdownComponent(markdownData)
    markdownRender.Draw()    
    



    

    

    














    
    







if __name__ == "__main__":
    main()

