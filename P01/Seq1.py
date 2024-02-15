class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases=None):
        # Initialize the sequence with the value
        # passed as argument when creating the object
        if strbases == None:
            self.strbases = "NULL"
            print("NULL sequence created")

        else:
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
        if self.strbases in ["NULL", "ERROR"]:
            length = 0
        else:
            length = len(self.strbases)
        return length

    def count_base(self, base):
        count = 0
        if self.strbases not in ["NULL", "ERROR"]:
            for b in self.strbases:
                if b == base:
                    count += 1

        return count

    def count(self):
        dictionary = {"A": 0, "C": 0, "T": 0, "G": 0}
        if self.strbases not in ["NULL", "ERROR"]:
            for e in self.strbases:
                dictionary[e] += 1
        return dictionary

    def reverse(self):
        rev = ""
        if self.strbases in ["NULL", "ERROR"]:
            rev = self.strbases
        else:
            for i in self.strbases:
                rev = i + rev
        return rev

    def complement(self):
        comp = ""
        c_dict = {"A": "T", "T": "A", "G": "C", "C": "G"}
        if self.strbases in ["NULL", "ERROR"]:
            comp = self.strbases
        else:
            for base in self.strbases:
                comp += c_dict[base]
        return comp

    def read_fasta(self, filename):
        from pathlib import Path
        folder = "../S04/sequences/"
        file_contents = Path(folder + filename).read_text()

        first_line = file_contents.find("\n")
        sequence = file_contents[first_line:].replace("\n", "")
        return sequence
