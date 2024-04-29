import http.client
import json
import termcolor

SERVER = "rest.ensembl.org"
ID = "ENSG00000207552"
ENDPOINT = "/sequence/id/"
PARAMS = "?content-type=application/json"

URL = SERVER + ENDPOINT + ID + PARAMS

print()
print(f"Server: {SERVER}")
print(f"URL: {URL}")

# Connect with the server
conn = http.client.HTTPConnection(SERVER)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
try:
    conn.request("GET", ENDPOINT + ID + PARAMS)
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

# -- Read the response message from the server
r1 = conn.getresponse()

# -- Print the status line
print(f"Response received!: {r1.status} {r1.reason}\n")

# -- Read the response's body
data1 = r1.read().decode("utf-8")

# -- Transform it into JSON format
g = json.loads(data1)

termcolor.cprint("Gene:", 'yellow', end='')
print("MIR633")

termcolor.cprint("Description:", 'yellow', end='')
print(g["desc"])

termcolor.cprint("Bases:", 'yellow', end='')
print(g["seq"])
