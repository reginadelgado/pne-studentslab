from pathlib import Path

FILENAME = "sequences/U5.txt"

file_contents = Path(FILENAME).read_text()

first_line = file_contents.find("\n")
header = file_contents[:first_line]
sequence = file_contents[first_line:].replace("\n", "", 1)

print("Body of the U5.txt file:\n" + sequence)