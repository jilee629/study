import pandas as pd

def test(i):
    if i == 1:
        data = {'name' : ['A', 'B', 'C'], 'id' : ['a', 'b', 'c'], 'age' : ['11', '12', '13']}
        df = pd.DataFrame(data)
        print(df)
        # name id age
        # 0    A  a  11
        # 1    B  b  12
        # 2    C  c  13
        print(df["age"][1])
        # 12
        print(df.loc[1]["age"])
        # 12
    
    if i == 2:
        data = [['A', 'a', '11'], ['B', 'b', '12'], ['C', 'c', '13']]
        columns = ['name', 'id', 'age']
        index = ['1', '2', '3']
        df = pd.DataFrame(data, columns=columns, index=index)
        print(df)
        #   name id age
        # 1    A  a  11
        # 2    B  b  12
        # 3    C  c  13

    if  i == 3:
        data = [('A', 'a', '11'), ('B', 'b', '12'), ('C', 'c', '13')]
        columns = ['name', 'id', 'age']
        index = ['1', '2', '3']
        df = pd.DataFrame(data, columns=columns, index=index)
        print(df)
        #   name id age
        # 1    A  a  11
        # 2    B  b  12
        # 3    C  c  13
        
        
if __name__ == "__main__":
    
    test(3)

