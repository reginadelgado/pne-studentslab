seq = input("Introduce the DNA sequence: ")

dictionary = {"A": 0, "C": 0, "T": 0, "G": 0}
for e in seq:
    dictionary[e] += 1

print("Total length:", len(seq))
for letter, count in dictionary.items():
    print(letter + ": " + str(count))
