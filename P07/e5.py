import http.client
import json
import termcolor
from Seq1 import Seq

genes = {"FRAT1": "ENSG00000165879", "ADA": "ENSG00000196839", "FXN": "ENSG00000165060", "RNU6_269P": "ENSG00000212379",
         "MIR633": "ENSG00000207552", "TTTY4C": "ENSG00000228296", "RBMY2YP": "ENSG00000227633", "FGFR3": "ENSG00000068078",
         "KDR": "ENSG00000128052", "ANK2": "ENSG00000145362"}


SERVER = "rest.ensembl.org"
ENDPOINT = "/sequence/id/"
PARAMS = "?content-type=application/json"

for gene in genes:
    ID = genes.get(gene)

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

    termcolor.cprint("Gene: ", 'yellow', end='')
    print(gene)

    termcolor.cprint("Description: ", 'yellow', end='')
    print(g["desc"])

    gene = Seq(g["seq"])

    termcolor.cprint("Total length: ", 'yellow', end='')
    print(gene.len())

    dict_bases = gene.count()

    mf_base = None
    higher_value = None
    for base, count in dict_bases.items():
        termcolor.cprint(f"{base}: ", 'blue', end='')
        print(f"{count} ({gene.percentage(base)})")
        if higher_value is None or count > higher_value:
            mf_base = base
            higher_value = count

    termcolor.cprint("Most frequent base: ", 'yellow', end='')
    print(mf_base)
