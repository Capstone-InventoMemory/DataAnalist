import pandas as pd

# 월별 데이터와 재고 데이터를 읽어옵니다.
def predict_sale(inventory_df):
    # 월별 데이터를 불러오기
    monthly_df = pd.read_csv('Monthly_InventoryData.csv', encoding='cp949')
    monthly_df.columns = monthly_df.columns.str.strip().str.lower()  # 열 이름 정리
    inventory_df.columns = [
        'item', 'incomingstock', 'outcomingstock', 'currentstock', 
        'incomingdate', 'currentoutcomingdate', 'leadtime', 
        'predictedsale', 'expectedusage', 'stddev', 
        'safestock', 'totalrequiredstock', 'servicelevel'
    ]
    inventory_df['item'] = inventory_df['item'].str.strip().str.lower()

    # 판매 예측을 계산하는 함수
    def predict_sale_for_item(monthlyData):
        if isinstance(monthlyData, pd.DataFrame):
            monthlyData = monthlyData.values.flatten()  # 2차원 배열을 1차원으로 평탄화

        # 데이터를 숫자로 변환하고, 변환할 수 없는 값은 NaN으로 처리한 후 NaN을 0으로 변경
        monthlyData = pd.to_numeric(monthlyData, errors='coerce')
        
        totalSales = monthlyData.sum()  # 월간 판매량 합계
        daysInMonth = len(monthlyData)  # 한 달 동안의 일수

        return totalSales / daysInMonth if daysInMonth > 0 else 0 

    # 각 재고 항목에 대해 예측된 판매량을 계산
    for index, row in inventory_df.iterrows():
        itemName = row['item']
        
        if itemName in monthly_df.columns:
            monthlyData = monthly_df[itemName]  # 해당 항목의 월별 데이터를 가져옵니다.

            if monthlyData is not None and not monthlyData.empty:
                predictedSale = predict_sale_for_item(monthlyData)  # 예측된 판매량 계산
                inventory_df.at[index, 'predictedsale'] = round(predictedSale)  # 소수점을 반올림하여 저장
            else:
                inventory_df.at[index, 'predictedsale'] = 0

    return inventory_df
