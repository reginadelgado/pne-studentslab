from Seq1 import Seq
from Client0 import Client
from termcolor import *

PRACTICE = 2
EXERCISE = 6

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

#IP uni: 212.128.255.82
#IP casa: 192.168.1.46

IP = "212.128.255.82" # your IP address
PORT = 8080
PORT2 = 8081


# -- Create a client object
c1 = Client(IP, PORT)
c2 = Client(IP, PORT2)

# -- Test the ping method
print(c1)
print(c2)

s = Seq()
s.read_fasta("FRAT1.txt")
seq = str(s)
print(f"Gene FRAT1: {s}")

m = colored("Sending FRAT1 Gene to the server, in fragments of 10 bases...", "yellow")
c1.talk(m)
c2.talk(m)

n1, n2 = 0, 10
for i in range(10):
    fragment = seq[n1:n2]
    msg = f"Fragment {i + 1}: {fragment}"
    print(msg)
    if i % 2 == 0:
        c1.talk(colored(msg, "yellow"))
    else:
        c2.talk(colored(msg, "yellow"))
    n1 += 10
    n2 += 10
