# list.append
list1 = ['a', 'b', 'c']
list2 = ['e', 'f', 'g']
list1.append(list2)
print('append:', list1)
# ['a', 'b', 'c', ['e', 'f', 'g']]


# list.extend

list3 = ['a', 'b', 'c']
list4 = ['e', 'f', 'g']
list3.extend(list4)
print('extend:', list3)
# ['a', 'b', 'c', 'e', 'f', 'g']


