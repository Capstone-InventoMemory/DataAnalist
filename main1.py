import pandas as pd
import math
from scipy.stats import norm
import tkinter as tk
from tkinter import filedialog
import predict_sale  # predict_sale 모듈 임포트
import Orderquantity

# 파일 선택 다이얼로그 열기
def open_file_dialog(title, multiple=False):
    root = tk.Tk()
    root.withdraw()  # 루트 창 숨기기
    if multiple:
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")], title=title)
        return file_paths
    else:
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")], title=title)
        return file_path

# 안전 재고를 계산하는 함수
def Safetystock(leadTime, stdDev, serviceLevel):
    if leadTime <= 0 or stdDev <= 0 or pd.isna(leadTime) or pd.isna(stdDev):
        return 0
    zScore = norm.ppf(serviceLevel)
    safeStock = zScore * stdDev * math.sqrt(leadTime)
    return math.ceil(safeStock)

# 발주 수량을 계산하는 함수
def OrderQuantity(currentStock, predictedSale, leadTime, safeStock):
    if pd.isna(currentStock) or pd.isna(predictedSale) or pd.isna(leadTime) or pd.isna(safeStock):
        return 0
    expectedUsage = predictedSale * leadTime
    totalRequiredStock = expectedUsage + safeStock 
    orderQuantity = totalRequiredStock - currentStock 
    return max(0, orderQuantity)

# 오류 처리 함수
def handle_error(message, exception):
    print(f"{message}: {exception}")

# CSV 파일 로드 함수
def load_csv_file(title):
    file_path = open_file_dialog(title)
    if not file_path:
        print(f"{title} 파일을 선택하지 않았습니다. 종료합니다.")
        return None
    try:
        df = pd.read_csv(file_path, encoding='cp949')
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        handle_error(f"{title} 파일을 읽는 중 오류 발생", e)
        return None

# 판매 예측을 계산하는 함수
def calculate_sales_predictions(df):
    try:
        df = predict_sale.predict_sale(df)
        df['predictedsale'] = df['predictedsale'].fillna(0)  # NaN 값을 0으로 처리
        return df
    except Exception as e:
        handle_error("판매 예측 계산 중 오류 발생", e)
        return None

# 안전 재고 및 발주 수량 계산 함수
def calculate_safe_stock_and_order_quantity(df, serviceLevel):
    try:
        df['safestock'] = df.apply(lambda row: Safetystock(row['leadtime'], row['stddev'], serviceLevel), axis=1)
        df['expectedusage'] = df['predictedsale'] * df['leadtime']
        df['totalrequiredstock'] = df['expectedusage'] + df['safestock']
        df['orderquantity'] = df.apply(lambda row: OrderQuantity(row['currentstock'], row['predictedsale'], row['leadtime'], row['safestock']), axis=1)
        return df
    except KeyError as e:
        handle_error("안전 재고 또는 발주 수량 계산 중 KeyError 발생", e)
        return None
    except Exception as e:
        handle_error("안전 재고 또는 발주 수량 계산 중 오류 발생", e)
        return None

# 메인 함수
def main():
    # 1단계: 재고 데이터 파일 로드
    inventory_df = load_csv_file("재고 데이터 CSV 파일을 선택하세요")
    if inventory_df is None:
        return

    # 2단계: 월별 데이터 파일 로드
    monthly_df = load_csv_file("최근 한 달 간의 출고량 데이터 CSV 파일을 선택하세요")
    if monthly_df is None:
        return

    # 3단계: 판매 예측 계산
    inventory_df = calculate_sales_predictions(inventory_df)
    if inventory_df is None:
        return

    # 4단계: 안전 재고 및 발주 수량 계산
    serviceLevel = 0.95
    inventory_df = calculate_safe_stock_and_order_quantity(inventory_df, serviceLevel)
    if inventory_df is None:
        return

    # 5단계: 계산 결과 출력
    print(inventory_df[['item', 'leadtime', 'currentstock', 'predictedsale', 'safestock', 
                        'expectedusage', 'totalrequiredstock', 'orderquantity']])

    # 6단계: 결과를 CSV 파일로 저장
    try:
        inventory_df.to_csv('Updated_Orderquantity_InventoryData.csv', index=False, encoding='cp949')
        print("결과가 'Updated_Orderquantity_InventoryData.csv' 파일로 저장되었습니다.")
    except Exception as e:
        handle_error("파일 저장 중 오류 발생", e)

if __name__ == "__main__":
    main()
