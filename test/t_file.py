import os

data = ['aa', '00']
file_path = os.path.join(os.path.dirname(__file__), "file.txt")

with open(file_path, "w") as f:
    f.write(' '.join(data))