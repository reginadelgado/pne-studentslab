import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import jinja2 as j
from Seq1 import Seq

# Define the Server's port
PORT = 8080


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True
def read_html_file(filename):
    contents = Path("html" + filename).read_text()
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

        if path == "/":
            # Open the form1.html file
            contents = Path('html/index.html').read_text()

            # Generating the response message
            self.send_response(200)  # -- Status line: OK!

        else:
            try:
                contents = read_html_file(path + ".html")
                if path == "/ping":
                    pass

                elif path == "/get":
                    s1 = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
                    s2 = "AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA"
                    s3 = "CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT"
                    s4 = "CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA"
                    s5 = "AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT"

                    seq_list = [s1, s2, s3, s4, s5]
                    n = arguments.get("n")[0]
                    seq = seq_list[int(n)]

                    contents = contents.render(context={"seq": seq, "n": n})

                elif path == "/gene":
                    name = arguments.get("name")[0]
                    filename = name + ".txt"
                    seq = Seq()
                    seq.read_fasta(filename)

                    contents = contents.render(context={"gene": seq, "name": name})

                elif path == "/operation":
                    seq = arguments.get("seq",[""])[0]

                self.send_response(200)

            except (FileNotFoundError, TypeError, IndexError):
                contents = Path("html/error.html").read_text()
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
