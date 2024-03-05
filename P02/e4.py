from Seq1 import Seq
from Client0 import Client
from termcolor import *

#IP uni: 212.128.255.82
#IP casa: 192.168.1.46

IP = "192.168.1.46" # your IP address
PORT = 8081

# -- Create a client object
c = Client(IP, PORT)

# -- Test the ping method
print(c)

gene_list = ["U5", "FRAT1", "ADA"]

for name in gene_list:
    msg = f"Sending {name} Gene to the server..."
    print(f"To Server: {colored(msg, 'blue')}")
    response = c.talk(msg)
    print(f"From Server\n\n{colored(response, 'yellow')}")

    gene = Seq()
    filename = name + ".txt"
    gene.read_fasta(filename)

    print(f"To Server: {colored(str(gene), 'blue')}")
    response2 = c.talk(str(gene))
    print(f"From Server\n\n{colored(response2, 'yellow')}")
