from Seq1 import Seq
from Client0 import Client

#IP uni: 212.128.255.82
#IP casa: 192.168.1.46

IP = "192.168.1.46" # your IP address
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

c1.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases...")
c2.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases...")

n1, n2 = 0, 10
for i in range(10):
    fragment = seq[n1:n2]
    msg = f"Fragment {i + 1}: {fragment}"
    print(msg)
    if i % 2 == 0:
        c1.talk(msg)
    else:
        c2.talk(msg)
    n1 += 10
    n2 += 10
