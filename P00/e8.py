from Seq0 import seq_read_fasta, seq_count

gene_list = ["U5", "ADA", "FRAT1", "FXN"]

print("----| EXERCISE 7 |----")

for gene in gene_list:
    filename = gene + ".txt"
    sequence = seq_read_fasta(filename)
    bases_dict = seq_count(sequence)

    mf_base = None
    higher_value = None
    for base, count in bases_dict.items():
        if higher_value is None or count > higher_value:
            mf_base = base
            higher_value = count

    print("Gene " + gene + ": Most frequent Base: " + mf_base)
