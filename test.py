import os

with open("C://unnamed.jpg", "rb") as f:
    byte = f.read()

with open("new.jpg", "wb") as f:
    f.write(byte)

# NEED TO GET RID OF ACCESS b' IN THE CREATED FILE!
