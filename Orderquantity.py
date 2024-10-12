import pandas as pd
import math
from scipy.stats import norm

# .csv 파일 불러오기 (인코딩 설정)
df = pd.read_csv('InventoryData.csv', encoding='cp949')

# 열 이름을 영어로 변경
df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 'currentoutcomingDate', 'leadTime', 'predictedSale', 'stdDev']