from Seq1 import Seq
from Client0 import Client

IP = "212.128.255.82" # your IP address
PORT = 8081

# -- Create a client object
c = Client(IP, PORT)

# -- Test the ping method
print(c)

s = Seq()
s.read_fasta("FRAT1.txt")

print(f"Gene FRAT1: {s}")
c.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases...")
for i in range(5):
    n1, n2 = 0, 10
    msg = f"Fragment {i + 1}: {s[n1:n2]}"
    n1 += 10
    n2 += 10
    print
