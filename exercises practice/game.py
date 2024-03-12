import socket
import random


class NumberGuesser:
    def __init__(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = []

    def guess(self, number):
        if number == self.secret_number:
            self.attempts.append(number)
            r = f"You won after {len(self.attempts)}"
        elif number > self.secret_number:
            self.attempts.append(number)
            r = "Higher"
        else:
            self.attempts.append(number)
            r = "Lower"
        return r


IP = "127.0.0.1"
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((IP, PORT))

s.listen()

game = NumberGuesser()

while True:
    try:
        print("Waiting for clients...")
        (c, address) = s.accept()

    except KeyboardInterrupt:
        print("Server stopped by the user")
        s.close()

        exit()

    else:

        print("A client has connected to the server!")

        # -- Read the message from the client
        # -- The received message is in raw bytes
        msg_raw = c.recv(2048)

        # -- We decode it for converting it
        # -- into a human-redeable string
        msg = msg_raw.decode()

        # -- Print the received message

        # -- Send a response message to the client
        response = game.guess(int(msg))

        # -- The message has to be encoded into bytes
        c.send(response.encode())

        # -- Close the data socket
        c.close()
