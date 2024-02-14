class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        # Initialize the sequence with the value
        # passed as argument when creating the object
        self.strbases = strbases

        count = 0
        for b in self.strbases:
            if b in ["A", "T", "G", "C"]:
                count += 1
        if count == len(self.strbases):
            print("New sequence created!")

        else:
            self.strbases = "ERROR"
            print("INCORRECT sequence detected")

    def __str__(self):
        """Method called when the object is being printed"""
        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)
import termcolor
def print_seqs(seq_list, color):
    for seq in seq_list:
        termcolor.cprint(f"Sequence {seq_list.index(seq)}: (Length: {seq.len()}) {seq}", color)
def generate_seqs(pattern, number):
    seq_list = []
    seq = ""
    for i in range(number):
        seq += pattern
        seq_list.append(Seq(seq))

    return seq_list

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

termcolor.cprint("List 1:", "blue")
print_seqs(seq_list1, "blue")

print()
termcolor.cprint("List 2:", "green")
print_seqs(seq_list2, "green")
