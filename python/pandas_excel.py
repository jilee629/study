import pandas as pd
from datetime import date

data = [
   ['2002', '2003', '2004'],
   ['2.2', '2,3', '3.5'],
   ['1,44M', '2.22M', '2.45M']
]
columns = ['Year', 'GDP rate', 'GDP']
index = ['1', '2', '3']
df = pd.DataFrame(data, columns=columns, index=index)

# today=date.today()
# print(today)
df.to_excel(f'{date.today()}.xlsx', engine='openpyxl')