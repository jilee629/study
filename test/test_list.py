L = ['a', 'b', 'c']

L.append('d')
print(L)
# ['a', 'b', 'c', 'd']

L.remove('c')
print(L)
# ['a', 'b', 'd']

L.insert(1, 'c')
print(L)
['a', 'c', 'b', 'd']

L.extend(['e'])
print(L)
['a', 'c', 'b', 'd', 'e']