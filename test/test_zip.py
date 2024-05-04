def test_zip(i):
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    
    if i == 1:
        print(zip(numbers, letters))
        # <zip object at 0x000002A8BEE83100>

    if i == 2:
        [print(d) for d in zip(numbers, letters)]
        # (1, 'A')
        # (2, 'B')
        # (3, 'C')

    if i == 3:
        print(list(zip(numbers, letters)))
        # [(1, 'A'), (2, 'B'), (3, 'C')]

    if i == 4:
        print(dict(zip(numbers, letters)))
        # {1: 'A', 2: 'B', 3: 'C'}

    if i == 5:
        num, let = zip(*(zip(numbers, letters)))
        print(num, let)
        # (1, 2, 3) ('A', 'B', 'C')
    
    if i == 6:
        [print(i, z) for i, z in enumerate(zip(numbers, letters))]
        # 0 (1, 'A')
        # 1 (2, 'B')
        # 2 (3, 'C')
        [print(z) for i, z in enumerate(zip(numbers, letters))]
        # (1, 'A')
        # (2, 'B')
        # (3, 'C')
        [print(z[1]) for i, z in enumerate(zip(numbers, letters))]
        # A
        # B
        # C

    if i == 7:
        for number, upper, lower in zip("12345", "ABCDE", "abcde"):
            print(number, upper, lower)
            # 1 A a
            # 2 B b
            # 3 C c
            # 4 D d
            # 5 E e        
   
if __name__ == "__main__":

    test_zip(8)