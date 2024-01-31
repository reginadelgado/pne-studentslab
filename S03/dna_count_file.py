sequence = ""
with open("dna.txt", "r") as f:
    for line in f:
        sequence += line.replace("\n", "")
def dna_count(seq):
    dictionary = {"A": 0, "C": 0, "T": 0, "G": 0}
    for e in seq:
        dictionary[e] += 1

    print("Total length:", len(seq))
    for letter, count in dictionary.items():
        print(letter + ": " + str(count))

dna_count(sequence)
