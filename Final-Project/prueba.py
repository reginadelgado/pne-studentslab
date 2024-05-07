import http.client
import json

#def c(path, specie=None,  )

SERVER = "rest.ensembl.org"
PARAMS = "?content-type=application/json"
ENDPOINT = "/info/species"

URL = SERVER + ENDPOINT + PARAMS

print(f"Server: {SERVER}")
print(f"URL: {URL}")

# Connect with the server
conn = http.client.HTTPConnection(SERVER)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
try:
    conn.request("GET", ENDPOINT + PARAMS)
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
response = json.loads(data1)

all_species = response["species"]

names = ""
print(f"The total number of species in esambl {len(all_species)}")
for i in range(10):
    s = all_species[i]
    n = s["display_name"]
    names += f"-{n}\n"
print(names)
