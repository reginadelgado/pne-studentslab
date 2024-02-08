from pathlib import Path

def seq_ping():
    print("OK")


def seq_read_fasta(filename):
    folder = "/pne-studentslab/S04/sequences/"
    file_contents = Path(filename).read_text()

    first_line = file_contents.find("\n")
    sequence = file_contents[first_line:].replace("\n", "", 1)

    print("The first 20 bases are:\n" + sequence[:20])
