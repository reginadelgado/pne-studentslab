import http.client
import json


def c(endpoint):
    server = "rest.ensembl.org"
    params = "?content-type=application/json"

    # Connect with the server
    conn = http.client.HTTPConnection(server)

    # -- Send the request message, using the GET method. We are
    # -- requesting the main page (/)
    try:
        conn.request("GET", endpoint + params)
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

    return response


endpoint = "/info/species"

species = c(endpoint)
all_species = species["species"]

names = ""
print(f"The total number of species in esambl {len(all_species)}")
for i in range(10):
    s = all_species[i]
    n = s["display_name"]
    names += f"-{n}\n"
print(names)
