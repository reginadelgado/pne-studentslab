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
def print_seqs(seq_list):
    for seq in seq_list:
        print(f"Sequence {seq_list.index(seq)}: (Length: {seq.len()}) {seq}")

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

print_seqs(seq_list)
