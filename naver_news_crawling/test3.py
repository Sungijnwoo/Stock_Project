import pandas as pd

a = pd.read_excel("code_KOSDAQ.xlsx")
b = a.loc[0:2, 'name']
for i in b:
    print(i)