import pandas as pd
import math
from scipy.stats import norm

df = pd.read_csv('Updated_Predict_InventoryData.csv', encoding='cp949')

df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 'currentoutcomingDate', 'leadTime', 'predictedSale', 'expectedUseage', 'stdDev', 'safeStock', 'totalRequriedStock', 'serviceLevel']

def Safetystock(averageSale, leadTime, stdDev, serviceLevel):
    if leadTime <= 0 or stdDev <= 0 or pd.isna(leadTime) or pd.isna(stdDev):
        return 0
    zScore = norm.ppf(serviceLevel)
    safeStock = zScore * stdDev * math.sqrt(leadTime)
    return math.ceil(safeStock)

averageSale = 100
stdDev = 15
serviceLevel = 0.95

df['safeStock'] = df.apply(lambda row: Safetystock(averageSale, row['leadTime'], stdDev, serviceLevel), axis=1)

print(df[['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 'currentoutcomingDate', 'leadTime', 'predictedSale', 'expectedUseage', 'stdDev', 'safeStock', 'totalRequriedStock', 'serviceLevel']])

df.to_csv('Updated_InventoryData.csv', index=False, encoding='cp949')
