from Seq0 import seq_reverse, seq_read_fasta

filename = "U5.txt"
sequence = seq_read_fasta(filename)
print("----| EXERCISE 6 |----")
print("Gene U5")
fragment = sequence[:20]
print("Fragment:", fragment)
print("Reverse:", seq_reverse(sequence, 20))
