import os
from libs import utilites

with open("C://unnamed.jpg", "rb") as f:
    byte = f.read()

packs_of_data = []

whole_data = b""

num_of_bytes = len(byte)
num_of_packs = num_of_bytes // 128
if num_of_bytes % 128 != 0:
    num_of_packs += 1
for x in range(num_of_packs):
    try:
        packs_of_data.append(byte[128*x:(128*(x + 1))] + f" | {str(x)}".encode())
    except IndexError:
        packs_of_data.append(byte[128*(num_of_packs-1):] + str(x).encode())

sorted_packs = [None] * num_of_packs

"""for data_pack in packs_of_data:
    data = data_pack[::-1]
    new_data = data[data.index(b" | ")+3:][::-1]
    num = data[:data.index(b" | ")][::-1]
    sorted_packs[int(num.decode())] = new_data"""

for data_entry in sorted_packs:
    whole_data += data_entry

with open("new.jpg", "wb") as f:
    f.write(whole_data)



# Concept works, time to bring into practise
