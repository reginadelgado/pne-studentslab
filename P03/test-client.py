import Client0

print(f"-----| Practice 3, Exercise 7 |------")

PORT = 8080
IP = "127.0.0.1"

c = Client0.Client(IP, PORT)

print(c)

print("* Testing PING")
response = c.talk("PING")
print(response)

print("* Testing GET")
for i in range(5):
    response = c.talk(f"GET {i}")
    print(f"GET {i}: {response}")

seq = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"

print("\n* Testing INFO")
response = c.talk(f"INFO {seq}")
print(response)

print("* Testing COMP")
response = c.talk(f"COMP {seq}")
print(f"SEQ: {seq}")
print(f"COMP: {response}")

print("\n* Testing REV")
response = c.talk(f"COMP {seq}")
print(f"SEQ: {seq}")
print(f"COMP: {response}")

gene_list = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

print("\n* Testing GENE")
for gene in gene_list:
    msg = f"GENE {gene}"
    response = c.talk(msg)
    print(msg)
    print(response + "\n")
