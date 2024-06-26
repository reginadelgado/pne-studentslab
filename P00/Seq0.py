from pathlib import Path
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    folder = "../S04/sequences/"
    file_contents = Path(folder + filename).read_text()

    first_line = file_contents.find("\n")
    sequence = file_contents[first_line:].replace("\n", "")
    count = 0
    for b in sequence:
        if b in ["A", "T", "G", "C"]:
            count += 1
    if count != len(sequence):
        sequence = "Not valid sequence"
    return sequence

def seq_len(seq):
    len_seq = len(seq)
    return len_seq

def seq_count_base(seq, base):
    count = 0
    for b in seq:
        if b == base:
            count += 1

    return count

def seq_count(seq):
    dictionary = {"A": 0, "C": 0, "T": 0, "G": 0}
    for e in seq:
        dictionary[e] += 1
    return dictionary

def seq_reverse(seq, n = None):
    new_seq = ""
    if n == None:
        for i in seq:
            new_seq = i + new_seq
    else:
        for i in range(n):
            new_seq = seq[i] + new_seq
    return new_seq

def seq_complement(seq):
    c_seq = ""
    c_dict = {"A": "T", "T": "A", "G": "C", "C": "G"}
    for base in seq:
        c_seq += c_dict[base]

    return c_seq
