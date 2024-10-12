import pandas as pd
import math
from scipy.stats import norm

# .csv 파일 불러오기 (인코딩 설정)
df = pd.read_csv('InventoryData.csv', encoding='cp949')

# 열 이름을 영어로 변경
df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 'currentoutcomingDate', 'leadTime', 'predictedSale', 'expectedUseage', 'stdDev', 'safeStock', 'orderQuantity', 'totalRequriedStock']

# 안전 재고 계산 함수
def Safetystock(averageSale, leadTime, stdDev, serviceLevel):
    if leadTime <= 0 or stdDev <= 0 or pd.isna(leadTime) or pd.isna(stdDev):  # leadTime과 stdDev가 NaN이거나 0 이하일 경우
        return 0
    zScore = norm.ppf(serviceLevel)  # 서비스 레벨에 해당하는 z-점수 계산
    safeStock = zScore * stdDev * math.sqrt(leadTime)  # 안전 재고 계산
    return math.ceil(safeStock)  # 올림하여 반환

# 예시 데이터
averageSale = 100  # 일일 평균 판매량 (예시)
stdDev = 15        # 수요의 표준 편차 (예시)
serviceLevel = 0.95  # 서비스 레벨 95%

# 각 품목별 리드 타임에 따라 안전 재고 계산
df['safeStock'] = df.apply(lambda row: Safetystock(averageSale, row['leadTime'], stdDev, serviceLevel), axis=1)

# 계산된 안전 재고 출력
print(df[['item', 'leadTime', 'safeStock']])

df.to_csv('Updated_InventoryData.csv', index=False, encoding='cp949')