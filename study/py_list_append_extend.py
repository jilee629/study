# list.append
print('='*40)
list1 = ['a', 'b', 'c']
list2 = ['e', 'f', 'g']
list1.append(list2)
print(list1)
'''
['a', 'b', 'c', ['e', 'f', 'g']]
'''

# list.extend
print('='*40)
list1 = ['a', 'b', 'c']
list2 = ['e', 'f', 'g']
list1.extend(list2)
print(list1)
'''
['a', 'b', 'c', 'e', 'f', 'g']
'''

