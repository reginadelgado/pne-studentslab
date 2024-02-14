from Seq0 import seq_count_base, seq_read_fasta

gene_list = ["U5", "ADA", "FRAT1", "FXN"]

print("----| EXCERCISE 4 |----")

for gene in gene_list:
    filename = gene + ".txt"
    sequence = seq_read_fasta(filename)

    print("\nGene " + gene + ":")
    bases_list = ["A", "C", "T", "G"]
    for base in bases_list:
        print(" " + base + ": " + str(seq_count_base(sequence, base)))
