d1 = ['a', 'b', 'c']
d2 = ['e', 'f', 'g']
d1.append(d2)
print(d1)
'''
['a', 'b', 'c', ['e', 'f', 'g']]
'''

d1 = ['a', 'b', 'c']
d2 = ['e', 'f', 'g']
d1.extend(d2)
print(d1)
'''
['a', 'b', 'c', 'e', 'f', 'g']
'''

d1 = ['a', 'b', 'c']
print(tuple(d1))
'''
('a', 'b', 'c')
'''