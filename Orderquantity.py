import pandas as pd
import math
from scipy.stats import norm

df = pd.read_csv('Updated_Predict_InventoryData.csv', encoding='cp949')

df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 
              'currentoutcomingDate', 'leadTime', 'predictedSale', 'stdDev', 
              'serviceLevel', 'safeStock', 'orderQuantity', 'totalRequiredStock']

print("NaN 값 수:", df.isna().sum())

df.fillna(0, inplace=True)

def Safetystock(averageSale, leadTime, stdDev, serviceLevel):
    if leadTime <= 0 or stdDev <= 0 or pd.isna(leadTime) or pd.isna(stdDev):
        return 0
    zScore = norm.ppf(serviceLevel)
    safeStock = zScore * stdDev * math.sqrt(leadTime)
    return math.ceil(safeStock)

def OrderQuantity(currentStock, predictedSale, leadTime, safeStock):
    if pd.isna(currentStock) or pd.isna(predictedSale) or pd.isna(leadTime) or pd.isna(safeStock):
        return 0
    expectedUsage = predictedSale * leadTime
    totalRequiredStock = expectedUsage + safeStock 
    orderQuantity = totalRequiredStock - currentStock 
    return max(0, orderQuantity)

averageSale = 100 
serviceLevel = 0.95

df['safeStock'] = df.apply(lambda row: Safetystock(averageSale, row['leadTime'], row['stdDev'], serviceLevel), axis=1)

df['expectedUsage'] = df['predictedSale'] * df['leadTime']
df['totalRequiredStock'] = df['expectedUsage'] + df['safeStock']
df['orderQuantity'] = df.apply(lambda row: OrderQuantity(row['currentStock'], row['predictedSale'], row['leadTime'], row['safeStock']), axis=1)

print(df[['item', 'leadTime', 'currentStock', 'predictedSale', 'safeStock', 
           'expectedUsage', 'totalRequiredStock', 'orderQuantity']])


df.to_csv('Updated_Orderquantity_InventoryData.csv', index=False, encoding='cp949')