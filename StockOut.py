import pandas as pd

df = pd.read_csv('InventoryData.csv', encoding='cp949')
df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 'currentoutcomingDate', 'leadTime', 'predictedSale', 'expectedUseage', 'stdDev', 'safeStock', 'orderQuantity', 'totalRequriedStock']

def Stockout(saleData, timePeriod):
    if timePeriod <= 0:
        raise ValueError("timePeriod must be greater than zero.")
    
    totalSales = sum(saleData)
    return totalSales / timePeriod

saleData = df['outcomingStock'].tolist()

timePeriod = len(df['currentoutcomingDate'].unique())

averageSales = Stockout(saleData, timePeriod)
print(f"기간 별 일일 평균 출고 수량: {averageSales:.2f}")