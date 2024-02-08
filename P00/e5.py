from Seq0 import seq_count, seq_read_fasta

gene_list = ["U5", "ADA", "FRAT1", "FXN"]

print("----| EXERCISE 5 |----")

for gene in gene_list:
    filename = gene + ".txt"
    sequence = seq_read_fasta(filename)

    bases_dict = seq_count(sequence)

    print("Gene " + gene + ": ", bases_dict)