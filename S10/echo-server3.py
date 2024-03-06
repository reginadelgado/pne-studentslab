import socket
from termcolor import *

# Configure the Server's IP and PORT
PORT = 8080
IP = "127.0.0.1" # the IP address depends on the machine running the server

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening
ls.listen()

print("The server is configured!")

number_con = 0
ip_port = []

while True:
    # -- Waits for a client to connect
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()

    # -- Server stopped manually
    except KeyboardInterrupt:
        print("Server stopped by the user")

        # -- Close the listenning socket
        ls.close()

        # -- Exit!
        exit()

    # -- Execute this part if there are no errors
    else:

        number_con += 1

        print(f"CONNECTION: {number_con}. From the IP: {client_ip_port}")
        # -- Read the message from the client
        # -- The received message is in raw bytes
        msg_raw = cs.recv(2048)

        # -- We decode it for converting it
        # -- into a human-redeable string
        msg = msg_raw.decode()

        # -- Print the received message
        print(f"Message received: {colored(msg, 'green')}")

        # -- Send a response message to the client
        response = f"ECHO: {msg}"

        # -- The message has to be encoded into bytes
        cs.send(response.encode())

        #add ip and port to the list
        ip_port.append(client_ip_port)

        if number_con == 5:
            print("The following clients has connected to the server:")
            for i in range(5):
                print(f"Client {i}: {ip_port[i]}")
            # -- Close the data socket
            cs.close()
            exit()