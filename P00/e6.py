from Seq0 import seq_reverse, seq_read_fasta

filename = "U5.txt"
sequence = seq_read_fasta(filename)
print("----| EXCERCISE 6 |----")
print("Gene U5")
print("Fragment:", sequence[:20])
print("Reverse:", seq_reverse(sequence, 20))