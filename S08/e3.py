import socket

# SERVER IP, PORT
PORT = 8081
IP = "212.128.255.81" # depends on the computer the server is running

while True:
    msg = input("Enter your message: ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    s.send(str.encode(msg))
    s.close()
    break
