from Seq1 import Seq
import socket
from termcolor import *

# Configure the Server's IP and PORT
PORT = 8080
IP = "127.0.0.1"  # the IP address depends on the machine running the server

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening
ls.listen()

print("SEQ Server is configured!")
s1 = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
s2 = "AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA"
s3 = "CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT"
s4 = "CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA"
s5 = "AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT"

seq_list = [s1, s2, s3, s4, s5]

while True:
    # -- Waits for a client to connect
    print("Waiting for Clients ...")

    try:
        (cs, client_ip_port) = ls.accept()

    # -- Server stopped manually
    except KeyboardInterrupt:
        print("Server stopped by the user")

        # -- Close the listening socket
        ls.close()

        # -- Exit!
        exit()

    # -- Execute this part if there are no errors
    else:

        # print("A client has connected to the server!")

        # -- Read the message from the client
        # -- The received message is in raw bytes
        msg_raw = cs.recv(2048)

        # -- We decode it for converting it
        # -- into a human-redeable string
        msg = msg_raw.decode()
        msg_l = msg.split(" ")

        command = msg_l[0]
        print(f"{colored(command, 'yellow')}")

        if command == "PING" and len(msg_l) == 1:
            response = "OK!"
            # command = "PING command!"

        elif len(msg_l) == 2:
            command = msg_l[0]
            if command == "GET":
                n_seq = msg_l[1]
                if n_seq.isdigit() and 0 <= int(n_seq) <= 4:
                    response = seq_list[int(n_seq)]

                else:
                    response = "Not valid number"

            elif command == "INFO":
                seq = Seq(msg_l[1])
                response = f"Sequence: {seq}\nTotal length: {seq.len()}\n"
                for i in ["A", "C", "G", "T"]:
                    response += f"{i}: {seq.count_base(i)} ({seq.percentage(i)})\n"

            elif command == "COMP":
                seq = Seq(msg_l[1])
                response = seq.complement()

            elif command == "REV":
                seq = Seq(msg_l[1])
                response = seq.reverse()

            elif command == "GENE":
                gene_name = msg_l[1]
                if gene_name in ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]:
                    filename = gene_name + ".txt"
                    seq = Seq()
                    seq.read_fasta(filename)
                    response = str(seq)
                else:
                    response = "Not valid Gene"

            else:
                response = "Unknown command"
        else:
            response = "Unknown command"

        print(response, "\n")
        # -- Send a response message to the client
        # response = f"ECHO: {msg}"

        # -- The message has to be encoded into bytes
        cs.send(response.encode())

        # -- Close the data socket
        cs.close()
