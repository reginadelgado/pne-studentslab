import http.server
import termcolor
import http.client
import json


def client(endpoint, params=""):
    port = 8080
    server = 'localhost'

    print(f"\nConnecting to server: {server}:{port}\n")

    # Connect with the server
    conn = http.client.HTTPConnection(server, port)

    # -- Send the request message, using the GET method. We are
    # -- requesting the main page (/)
    try:
        conn.request("GET", endpoint + f'?{params}json=1')
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


def handle_response(response):
    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        return response


def list_species(limit=None):
    if limit:
        params = f"limit={limit}&"
    else:
        params = ""

    response = client("/listSpecies", params)
    response = handle_response(response)
    if response:
        species_names = response.get("species_names")
        print(f"The limit you have selected is: {limit}")
        print("List of species:")
        for name in species_names:
            print(f"- {name}")


def karyotype(species):
    response = client("/karyotype", f"species={species}&")
    response = handle_response(response)
    if response:
        print(f"Karyotype for {species}:")
        karyotype = response.get("karyotype")
        for k in karyotype:
            print(f"- {k}")


def chromosome_length(species, chromo):
    response = client("/chromosomeLength", f"species={species}&chromo={chromo}&")
    response = handle_response(response)
    if response:
        length = response.get("length")
        print(f"Length of chromosome {chromo} in {species}: {length}")


def gene_sequence(gene):
    response = client("/geneSeq", f"gene={gene}&")
    response = handle_response(response)
    if response:
        seq = response.get("seq")
        print(f"Sequence of gene {gene}: {seq}")


def gene_info(gene):
    response = client("/geneInfo", f"gene={gene}&")
    response = handle_response(response)
    if response:
        print(f"Information for gene {gene}:\n")
        for key in response:
            print(f"{key.capitalize()}: {response.get(key)}")


def gene_calc(gene):
    response = client("/geneCalc", f"gene={gene}&")
    response = handle_response(response)
    if response:
        print(f"Calculations for gene {gene}:\n")
        for key in response:
            print(f"{key.capitalize()}: {response.get(key)}")


def gene_list(chromo, start, end):
    response = client("/geneList", f"chromo={chromo}&start={start}&end={end}&")
    response = handle_response(response)
    if response:
        genes = response.get("genes")
        print(f"Genes in region {chromo}:{start}-{end}:")
        for gene in genes:
            print(f"- {gene}")


#list_species(10)
#list_species()
#karyotype("mouse")
#chromosome_length("mouse", "18")
#gene_sequence("FRAT1")
gene_info("FRAT1")
gene_calc("FRAT1")
gene_list("9", 22125500, 22136000)

#igual añadir que las keys de los diccionarios sean los nombres de los genes