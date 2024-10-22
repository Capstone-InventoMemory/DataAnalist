import pandas as pd
import math
from scipy.stats import norm

# CSV 파일 로드
df = pd.read_csv('Updated_Predict_InventoryData.csv', encoding='cp949')

# 컬럼 이름 설정
df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 
              'currentoutcomingDate', 'leadTime', 'predictedSale', 'expectedUsage', 
              'stdDev', 'safeStock', 'totalRequiredStock', 'serviceLevel']
df.rename(columns={'Lead Time': 'leadTime'}, inplace=True)
# NaN 값 처리
df.fillna(0, inplace=True)

# 안전 재고 계산 함수
def Safetystock(leadTime, stdDev, serviceLevel):
    try:
        if leadTime <= 0 or stdDev <= 0:
            return 0
        zScore = norm.ppf(serviceLevel)
        safeStock = zScore * stdDev * math.sqrt(leadTime)
        return math.ceil(safeStock)
    except Exception as e:
        print(f"안전 재고 계산 중 오류 발생: {e}")
        return 0

# 발주 수량 계산 함수
def OrderQuantity(currentStock, predictedSale, leadTime, safeStock):
    try:
        expectedUsage = predictedSale * leadTime
        totalRequiredStock = expectedUsage + safeStock
        orderQuantity = totalRequiredStock - currentStock
        return max(0, orderQuantity)
    except Exception as e:
        print(f"발주 수량 계산 중 오류 발생: {e}")
        return 0

# 서비스 레벨 설정
serviceLevel = 0.95

# 안전 재고 계산
df['safeStock'] = df.apply(lambda row: Safetystock(row['leadTime'], row['stdDev'], serviceLevel), axis=1)

# 예상 소진량 및 발주 수량 계산
df['expectedUsage'] = df['predictedSale'] * df['leadTime']
df['totalRequiredStock'] = df['expectedUsage'] + df['safeStock']
df['orderQuantity'] = df.apply(lambda row: OrderQuantity(row['currentStock'], row['predictedSale'], row['leadTime'], row['safeStock']), axis=1)

# 계산된 값 확인
print(df[['item', 'leadTime', 'currentStock', 'predictedSale', 'safeStock', 
           'expectedUsage', 'totalRequiredStock', 'orderQuantity']])

# 결과를 CSV 파일로 저장
df.to_csv('Updated_Orderquantity_InventoryData.csv', index=False, encoding='cp949')
