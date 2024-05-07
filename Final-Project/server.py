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


def read_html_file(filename):
    contents = Path(filename).read_text()
    contents = j.Template(contents)
    return contents


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
                    endpoint = "/info/assembly/" + species_name
                    species = c(endpoint)
                    karyotype = species["karyotype"]
                    k_names = ""
                    for k in karyotype:
                        k_names += f"{k}<br>"
                    t = f"The names of the chromosomes are: <br><br> {k_names}"
                    contents = contents.render(context={"t": t})

                self.send_response(200)

            except (FileNotFoundError, TypeError, IndexError, ConnectionRefusedError):
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

