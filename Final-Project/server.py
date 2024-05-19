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

    # -- Send the request message, using the GET method.
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
    contents = Path(f"html/{filename}").read_text()
    contents = j.Template(contents)
    return contents


def get_gene_id(gene_name):
    endpoint = "/xrefs/symbol/homo_sapiens/" + gene_name
    gene_info = c(endpoint)
    g_id = ""
    for e in gene_info:
        if len(e["id"]) == 15 and e["type"] == "gene":
            g_id = e["id"]

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

        json_requested = False
        if arguments.get("json") and arguments.get("json")[0] == "1":
            json_requested = True

        content_type = 'text/html'

        if json_requested:
            content_type = 'application/json'

        contents = ""

        if path == "/":
            contents = Path('html/main_page.html').read_text()

            self.send_response(200)  # -- Status line: OK!

        else:
            try:
                error_code = 200
                if path == "/listSpecies":
                    endpoint = "/info/species"
                    species = c(endpoint)
                    all_species = species["species"]
                    limit = arguments.get("limit")

                    if limit:
                        limit = int(limit[0])
                    else:
                        limit = len(all_species)

                    l_names = []
                    for e in all_species[:limit]:
                        l_names.append(e["display_name"])

                    if json_requested:
                        contents = json.dumps({"species_names": l_names})

                    else:
                        contents = read_html_file("listSpecies.html")
                        names = ""
                        for s in l_names:
                            names += f"-{s}<br>"

                        contents = contents.render(context={"allspecies": len(all_species), "limit": limit,
                                                            "names": names})

                elif path == "/karyotype":
                    species_name = arguments.get("species")[0].lower()
                    name = species_name.replace(" ", "_")
                    endpoint = f"/info/assembly/{name}"
                    species = c(endpoint)
                    karyotype = species["karyotype"]

                    if json_requested:
                        contents = {"species": species_name, "karyotype": karyotype}
                        contents = json.dumps(contents)

                    else:
                        contents = read_html_file("karyotype.html")
                        k_names = ""
                        for k in karyotype:
                            k_names += f"{k}<br>"
                        contents = contents.render(context={"k_names": k_names, "species": species_name})

                elif path == "/chromosomeLength":
                    species_name = arguments.get("species")[0].lower()
                    name = species_name.replace(" ", "_")
                    endpoint = f"/info/assembly/{name}"
                    species = c(endpoint)
                    c_name = arguments.get("chromo")[0]

                    tlr = species["top_level_region"]
                    length = 0
                    for e in tlr:
                        name = e["name"]
                        if name == c_name:
                            length = e["length"]
                            break

                    if json_requested:
                        if length == 0:
                            contents = {"error": "The data you entered does not exist in the ensembl"}
                        else:
                            contents = {"species": species_name, "chromo": c_name, "length": length}

                        contents = json.dumps(contents)

                    else:
                        if length == 0:
                            contents = Path("html/error.html").read_text()
                            error_code = 404

                        else:
                            contents = read_html_file("chromosome.html")
                            contents = contents.render(context={"species": species_name, "chromo": c_name,
                                                                "len": length})

                elif path == "/geneSeq":
                    g_name = arguments.get("gene")[0]
                    g_id = get_gene_id(g_name)

                    endpoint = f"/sequence/id/{g_id}"
                    gene = c(endpoint)
                    seq = gene["seq"]

                    if json_requested:
                        contents = {"name": g_name, "seq": seq}
                        contents = json.dumps(contents)

                    else:
                        contents = read_html_file("geneSeq.html")
                        contents = contents.render(context={"gene": seq, "name": g_name})

                elif path == "/geneInfo":
                    g_name = arguments.get("gene")[0]
                    g_id = get_gene_id(g_name)

                    endpoint = f"/lookup/id/{g_id}"
                    info = c(endpoint)
                    start = info.get("start")
                    end = info.get("end")
                    chromo = info.get("seq_region_name")
                    length = int(end) - int(start) + 1

                    if json_requested:
                        contents = {"name": g_name, "id": g_id, "start": start, "end": end, "chromo": chromo,
                                    "length": length}
                        contents = json.dumps(contents)

                    else:
                        contents = read_html_file("geneInfo.html")
                        contents = contents.render(
                            context={"name": g_name, "start": start, "end": end, "chromo": chromo,
                                     "length": length, "id": g_id})

                elif path == "/geneCalc":
                    g_name = arguments.get("gene")[0]
                    g_id = get_gene_id(g_name)

                    endpoint = f"/sequence/id/{g_id}"
                    gene = c(endpoint)
                    seq = gene["seq"]
                    seq = Seq(seq)
                    length = seq.len()

                    p_dict = {"A": seq.percentage("A"), "T": seq.percentage("T"), "G": seq.percentage("G"),
                              "C": seq.percentage("C")}

                    if json_requested:
                        contents = {"name": g_name, "length": length, "percentages": p_dict}
                        contents = json.dumps(contents)

                    else:
                        contents = read_html_file("geneCalc.html")
                        percentages = ""
                        for b in p_dict:
                            percentages += f"{b}: {p_dict[b]} <br>"

                        contents = contents.render(context={"length": length, "percentages": percentages,
                                                            "name": g_name})

                elif path == "/geneList":
                    chromo = arguments.get("chromo")[0]
                    start = arguments.get("start")[0]
                    end = arguments.get("end")[0]

                    endpoint = f"/overlap/region/human/{chromo}:{start}-{end}"
                    extra_params = "feature=gene;feature=transcript;feature=cds;feature=exon;"

                    region = c(endpoint, extra_params)

                    names_list = []
                    for e in region:
                        if e["feature_type"] == "gene":
                            if e.get("external_name"):
                                names_list.append(e.get("external_name"))

                    if len(names_list) == 0:
                        names_list = ["No genes in the selected region"]

                    if json_requested:
                        contents = {"chromo": chromo, "start": start, "end": end, "genes": names_list}
                        contents = json.dumps(contents)

                    else:
                        contents = read_html_file("geneList.html")
                        names = ""
                        for g in names_list:
                            names += f"- {g} <br>"

                        contents = contents.render(context={"chromo": chromo, "start": start, "end": end,
                                                            "genes": names})

                self.send_response(error_code)

            except (FileNotFoundError, TypeError, IndexError, ConnectionRefusedError, KeyError, AttributeError,
                    ValueError):
                if json_requested:
                    contents = {"error": "The data you entered does not exist in the ensembl"}

                else:
                    contents = Path("html/error.html").read_text()

                self.send_response(404)

        # Define the content-type header:
        self.send_header('Content-Type', content_type)
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
