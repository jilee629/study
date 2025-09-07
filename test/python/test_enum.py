def enum1():
    for i, letter in enumerate(['A', 'B', 'C']):
        print(i, letter)   

def enum2():
    for entry in enumerate(['A', 'B', 'C']):
        print(entry)


if __name__ == "__main__":
    
    enum1()
    # 0 A
    # 1 B
    # 2 C

    enum2()
    # (0, 'A')
    # (1, 'B')
    # (2, 'C')