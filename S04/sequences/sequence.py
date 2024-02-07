from pathlib import Path

FILENAME = "ADA.txt"

file_contents = Path(FILENAME).read_text()

first_line = file_contents.find("\n")
header = file_contents[:first_line]
sequence = file_contents[first_line:].replace("\n", "")

print("The total number of basis of the sequence is:" + str(len(sequence)))
