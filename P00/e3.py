from Seq0 import seq_len, seq_read_fasta

gene_list = ["U5", "ADA", "FRAT1", "FXN"]
folder = "../S04/sequences/"

print("----| EXCERCISE 3 |----")

for gene in gene_list:
    filename = gene + ".txt"
    sequence = seq_read_fasta(filename)
    print("Gene " + gene + " -> Length: " + str(seq_len(sequence)))
