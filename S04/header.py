from pathlib import Path

FILENAME = "sequences/RNU6_269P.txt"

file_contents = Path(FILENAME).read_text()

first_line = file_contents.find("\n")
header = file_contents[:first_line]

print("First line of the RNU6_269P.txt file:\n" + header)
