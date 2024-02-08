from Seq0 import seq_read_fasta

filename = input("DNA file: ")
sequence = seq_read_fasta(filename)

print("The first 20 bases are:\n" + sequence[:20])