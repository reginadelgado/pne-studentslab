from Seq1 import Seq
print("-----| Practice 1, Exercise 3 |------")
# -- Create a Null sequence
s1 = Seq()

# -- Create a valid sequence
s2 = Seq("ACTGA")

# -- Create an invalid sequence
s3 = Seq("Invalid sequence")

seq_list = [s1, s2, s3]

for seq in seq_list:
    print(f"Sequence {seq_list.index(seq) + 1}: {seq}")
