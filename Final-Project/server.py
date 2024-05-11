import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import jinja2 as j
import http.client
import json

from Seq1 import Seq

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


def c(endpoint, extra_params=""):
    server = "rest.ensembl.org"
    params = f"?{extra_params}content-type=application/json"

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


def read_html_file(filename):
    contents = Path(filename).read_text()
    contents = j.Template(contents)
    return contents


def get_gene_id(gene_name):
    endpoint = "/xrefs/symbol/homo_sapiens/" + gene_name
    gene_info = c(endpoint)
    g_id = ""
    for e in gene_info:
        if len(e.get("id")) == 15:
            g_id = e.get("id")

    return g_id


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path)
        path = url_path.path
        arguments = parse_qs(url_path.query)
        json_requested = "json" in arguments and arguments["json"][0] == "1"
        contents = ""

        if path == "/":
            # Open the form1.html file
            contents = Path('main_page.html').read_text()

            # Generating the response message
            self.send_response(200)  # -- Status line: OK!

        else:
            try:
                if path == "/listSpecies":
                    contents = read_html_file("listSpecies.html")
                    endpoint = "/info/species"
                    species = c(endpoint)
                    all_species = species["species"]
                    limit = arguments.get("limit")

                    if limit:
                        limit = limit[0]
                    else:
                        limit = len(all_species)

                    names = ""
                    for i in range(int(limit)):
                        s = all_species[i]
                        n = s["display_name"]
                        names += f"-{n}<br>"

                    contents = contents.render(context={"allspecies": len(all_species), "limit": limit, "names": names})

                elif path == "/karyotype":
                    contents = read_html_file("karyotype.html")
                    species_name = arguments.get("species")[0]
                    species_name = species_name.replace(" ", "_")
                    endpoint = f"/info/assembly/{species_name}"
                    species = c(endpoint)
                    karyotype = species["karyotype"]
                    k_names = ""
                    for k in karyotype:
                        k_names += f"{k}<br>"
                    contents = contents.render(context={"k_names": k_names})

                elif path == "/chromosomeLength":
                    contents = read_html_file("chromosome.html")
                    species_name = arguments.get("species")[0].lower()
                    species_name = species_name.replace(" ", "_")
                    endpoint = f"/info/assembly/{species_name}"
                    species = c(endpoint)
                    c_name = arguments.get("chromo")[0]

                    tlr = species.get("top_level_region")
                    length = 0
                    for e in tlr:
                        name = e.get("name")
                        cs = e.get("coord_system")
                        if cs == "chromosome" and name == c_name:
                            length = e.get("length")

                    contents = contents.render(context={"len": length})

                elif path == "/geneSeq":
                    contents = read_html_file("geneSeq.html")
                    g_name = arguments.get("gene")[0]
                    g_id = get_gene_id(g_name)

                    endpoint = f"/sequence/id/{g_id}"
                    gene = c(endpoint)
                    seq = gene["seq"]
                    contents = contents.render(context={"gene": seq, "name": g_name})

                elif path == "/geneInfo":
                    contents = read_html_file("geneInfo.html")
                    g_name = arguments.get("gene")[0]
                    g_id = get_gene_id(g_name)

                    endpoint = f"/lookup/id/{g_id}"
                    info = c(endpoint)
                    start = info.get("start")
                    end = info.get("end")
                    chromo = info.get("seq_region_name")
                    length = int(end) - int(start)

                    contents = contents.render(context={"name": g_name, "start": start, "end": end, "chromo": chromo,
                                                        "length": length, "id": g_id})
                elif path == "/geneCalc":
                    contents = read_html_file("geneCalc.html")
                    g_name = arguments.get("gene")[0]
                    g_id = get_gene_id(g_name)

                    endpoint = f"/sequence/id/{g_id}"
                    gene = c(endpoint)
                    seq = gene["seq"]
                    seq = Seq(seq)
                    length = seq.len()

                    p_dict = {"A": seq.percentage("A"), "T": seq.percentage("T"), "G": seq.percentage("G"),
                              "C": seq.percentage("C")}

                    percentages = ""
                    for b in p_dict:
                        percentages += f"{b}: {p_dict[b]} <br>"

                    contents = contents.render(context={"length": length, "percentages": percentages, "name": g_name})

                elif path == "/geneList": #arreglar
                    contents = read_html_file("geneList.html")
                    chromo = arguments.get("chromo")
                    start = arguments.get("start")
                    end = arguments.get("end")

                    endpoint = f"/overlap/region/human/{chromo}:{start}-{end}"
                    extra_params = "feature=gene;feature=transcript;feature=cds;feature=exon;"
                    gene_dict = c(endpoint, extra_params)

                    print(gene_dict)
                    names_list = []
                    for g in gene_dict:
                        names_list.append(g.get("external_name"))

                    names = ""
                    for g in names_list:
                        names += f"- {g} <br>"

                    contents = contents.render(context={"chromo": chromo, "start": start, "end": end, "genes": names})

                self.send_response(200)

            except (FileNotFoundError, TypeError, IndexError, ConnectionRefusedError, KeyError):
                contents = Path("error.html").read_text()
                self.send_response(404)

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
