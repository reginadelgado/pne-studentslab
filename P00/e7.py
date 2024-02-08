from Seq0 import seq_complement, seq_read_fasta

filename = "U5.txt"
sequence = seq_read_fasta(filename)
print("----| EXERCISE 7 |----")
print("Gene U5")
fragment = sequence[:20]
print("Frag:", fragment)
print("Comp:", seq_complement(fragment))
