from Seq1 import Seq

gene_list = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

print("-----| Practice 1, Exercise 10 |------")

for name in gene_list:
    gene = Seq()
    filename = name + ".txt"
    gene.read_fasta(filename)
    bases_dict = gene.count()

    mf_base = None
    higher_value = None
    for base, count in bases_dict.items():
        if higher_value is None or count > higher_value:
            mf_base = base
            higher_value = count

    print("Gene " + name + ": Most frequent Base: " + mf_base)
