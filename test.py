import pandas as pd

# .csv 파일 불러오기
df = pd.read_csv('InventoryData.csv', encoding='cp949')

# 현재 DataFrame의 열 이름과 개수 출력
print(df.columns)
print("Number of columns:", len(df.columns))