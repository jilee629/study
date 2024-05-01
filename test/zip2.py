numbers = [1, 2, 3]
letters = ["A", "B", "C"]

for i, z in enumerate(zip(numbers, letters)):
    print(i, z)
    print(z)
    print(z[0])
    print(z[1])