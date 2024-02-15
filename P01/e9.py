from Seq1 import Seq
print("-----| Practice 1, Exercise 9 |------")
# -- Create a Null sequence
s = Seq()

# -- Initialize the null seq with the given file in fasta format
s1 = Seq(s.read_fasta("U5.txt"))

print(f"Sequence: (Length: {s1.len()}) {s1}")
print("Bases:", s1.count())
print("Rev:", s1.reverse())
print("Comp:", s1.complement())
