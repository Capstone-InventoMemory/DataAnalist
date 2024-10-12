import pandas as pd
import math
from scipy.stats import norm

# .csv 파일 불러오기 (인코딩 설정)
df = pd.read_csv('InventoryData.csv', encoding='cp949')

# 열 이름을 영어로 변경
df.columns = ['item', 'incomingStock', 'outcomingStock', 'currentStock', 'incomingDate', 'currentoutcomingDate', 'leadTime', 'predictedSale', 'stdDev']

# 안전 재고 계산 함수
def Safetystock(averageSale, leadTime, stdDev, serviceLevel):
    """
    averageSale: 일일 평균 판매량
    leadTime: 리드 타임(재고 주문 시 걸리는 시간)
    stdDev: 수요 표준 편차
    serviceLevel: 서비스 레벨 (ex: 0.95)
    
    return: 안전 재고 수준
    """
    zScore = norm.ppf(serviceLevel)  # 서비스 레벨에 따른 Z 점수 계산
    safeStock = zScore * stdDev * math.sqrt(leadTime)  # 안전 재고 계산식
    return math.ceil(safeStock)  # 소수점 반올림

# 예시 데이터
averageSale = 100  # 일일 평균 판매량 (예시)
stdDev = 15        # 수요의 표준 편차 (예시)
serviceLevel = 0.95  # 서비스 레벨 95%

# 각 품목별 리드 타임에 따라 안전 재고 계산
df['safeStock'] = df.apply(lambda row: Safetystock(averageSale, row['leadTime'], stdDev, serviceLevel), axis=1)

# 계산된 안전 재고 출력
print(df[['item', 'leadTime', 'safeStock']])
