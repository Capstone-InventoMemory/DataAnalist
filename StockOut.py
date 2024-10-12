import pandas as pd

df = pd.read_csv('InventoryData.csv', encoding='cp949')
df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 'currentoutcomingDate', 'leadTime', 'predictedSale', 'expectedUseage', 'stdDev', 'safeStock', 'orderQuantity', 'totalRequriedStock']

def Stockout(saleData, timePeriod):
    if timePeriod <= 0:
        raise ValueError("timePeriod must be greater than zero.")
    
    totalSales = sum(saleData)  # 총 출고 수량 합산
    return totalSales / timePeriod  # 일일 평균 출고 수량 계산

saleData = df['outcomingStock'].tolist()  # .csv 파일에서 출고 수량 리스트로 변환

# 분석 기간 (날짜 수)
timePeriod = len(df['currentoutcomingDate'].unique())  # 고유한 날짜 수 계산

# 기간 별 출고 수량 계산
averageSales = Stockout(saleData, timePeriod)
print(f"기간 별 일일 평균 출고 수량: {averageSales:.2f}")