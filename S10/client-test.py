import socket
from termcolor import *
from Client0 import Client

# -- Parameters of the server to talk to
IP = "127.0.0.1" # your IP address
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)


for i in range(5):
    msg = f"Message {i}"
    print(f"To Server: {colored(msg, 'blue')}")
    response = c.talk(colored(msg, 'yellow'))
    print(f"From Server: {colored(response, 'yellow')}")

