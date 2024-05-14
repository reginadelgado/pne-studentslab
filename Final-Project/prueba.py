import http.client
import json


SERVER = "rest.ensembl.org"
PARAMS = "?feature=gene;feature=transcript;feature=cds;feature=exon;content-type=application/json"
ENDPOINT = "/overlap/region/human/7:140424943-140624564"

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
print(response)
for e in response:
    if e.get("feature_type") == "gene":
        if e.get("external_name"):
            print(e.get("external_name"))

