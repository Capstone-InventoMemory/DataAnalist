import pandas as pd
import math
from scipy.stats import norm
import tkinter as tk
from tkinter import filedialog
import SafetyStock  # SafetyStock 모듈 임포트
import predict_sale  # predict_sale 모듈 임포트

# 파일 선택 다이얼로그 열기
def open_file_dialog(title):
    root = tk.Tk()
    root.withdraw()  # 루트 창 숨기기
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")], title=title
    )
    return file_path

# 안전 재고를 계산하는 함수
def calculate_safety_stock(df, stdDev=15, serviceLevel=0.95):
    # 'predictedsale' 컬럼이 있는지 확인
    if 'predictedsale' not in df.columns:
        print("'predictedsale' 컬럼이 없습니다.")
        return df
    
    df['safestock'] = df.apply(lambda row: SafetyStock.Safetystock(row['predictedsale'], row['leadtime'], stdDev, serviceLevel), axis=1)
    return df

# 예측 소진량 계산 (예상 판매량과 리드타임을 곱함)
def ExpectedUsage(predictedSale, leadTime):
    if predictedSale <= 0 or pd.isna(predictedSale):
        return 0
    return predictedSale * leadTime

# 메인 함수
def main():
    # 1단계: 사용자가 재고 데이터를 담은 CSV 파일을 선택하게 함
    csv_file_path = open_file_dialog("재고 데이터 CSV 파일을 선택하세요")
    if not csv_file_path:
        print("파일을 선택하지 않았습니다. 종료합니다.")
        return

    # 2단계: 선택한 파일을 읽어옴
    df = pd.read_csv(csv_file_path, encoding='cp949')
    df.columns = df.columns.str.strip().str.lower()  # 열 이름 정리

    # 3단계: 최근 한 달 간의 출고량 데이터가 담긴 파일 선택
    monthly_csv_path = open_file_dialog("최근 한 달 간의 출고량 데이터 CSV 파일을 선택하세요")
    if not monthly_csv_path:
        print("월별 출고량 파일을 선택하지 않았습니다. 종료합니다.")
        return
    
    monthly_df = pd.read_csv(monthly_csv_path, encoding='cp949')
    monthly_df.columns = monthly_df.columns.str.strip().str.lower()  # 열 이름 정리

    # 4단계: 판매 예측 계산
    df = predict_sale.predict_sale(df)  # 예측된 판매량을 계산

    # 예측된 판매량이 제대로 계산되었는지 확인
    if df['predictedsale'].isnull().any():
        print("예측된 판매량에 NaN 값이 있습니다. 예측 결과를 확인하세요.")
        df['predictedsale'] = df['predictedsale'].fillna(0)  # NaN 값을 0으로 처리

    # 5단계: 안전 재고 계산 (SafetyStock 함수 추가 필요)
    df = calculate_safety_stock(df)  # 안전 재고 계산

    # 6단계: 예상 소진량 계산
    df['expectedusage'] = df.apply(
        lambda row: round(ExpectedUsage(row['predictedsale'], row['leadtime']), 1), axis=1 
    )

    # 7단계: 결과 출력 (혹은 새로운 CSV로 저장)
    print("업데이트된 재고 데이터:")
    print(df[['item', 'predictedsale', 'expectedusage', 'safestock']])

    # 결과를 새로운 CSV 파일로 저장
    df.to_csv('Updated_InventoryData_with_predictions_safe.csv', index=False, encoding='cp949')

if __name__ == "__main__":
    main()