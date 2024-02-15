from Seq1 import Seq
print("-----| Practice 1, Exercise 2 |------")
# -- Creating a Null sequence
s1 = Seq()
# -- Creating a valid sequence
s2 = Seq("TATAC")

seq_list = [s1, s2]

for seq in seq_list:
    print(f"Sequence {seq_list.index(seq) + 1}: {seq}")
