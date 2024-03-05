from Seq1 import Seq
from Client0 import Client

#IP uni: 212.128.255.82
#IP casa: 192.168.1.46

IP = "192.168.1.46" # your IP address
PORT = 8081

# -- Create a client object
c = Client(IP, PORT)

# -- Test the ping method
print(c)

s = Seq()
s.read_fasta("FRAT1.txt")
seq = str(s)
print(f"Gene FRAT1: {s}")
c.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases...")
n1, n2 = 0, 10
for i in range(5):
    fragment = seq[n1:n2]
    msg = f"Fragment {i + 1}: {fragment}"
    print(msg)
    c.talk(msg)
    n1 += 10
    n2 += 10
