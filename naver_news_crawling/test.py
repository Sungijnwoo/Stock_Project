import pandas as pd

df = pd.read_excel("네이버뉴스_본문_22000.xlsx")

print(df.head())
df = df.drop([1])
print(df.head())