import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from scipy.stats import norm
import math

# 판매 예측을 계산하는 함수
def predict_sale_for_item(monthlyData):
    if isinstance(monthlyData, pd.DataFrame):
        monthlyData = monthlyData.values.flatten()

    monthlyData = pd.to_numeric(monthlyData, errors='coerce')
    totalSales = monthlyData.sum()
    daysInMonth = len(monthlyData)

    return totalSales / daysInMonth if daysInMonth > 0 else 0

# 안전 재고 계산 함수
def Safetystock(averageSale, leadTime, stdDev, serviceLevel):
    if leadTime <= 0 or stdDev <= 0 or pd.isna(leadTime) or pd.isna(stdDev):
        return 0
    zScore = norm.ppf(serviceLevel)
    safeStock = zScore * stdDev * math.sqrt(leadTime)
    return math.ceil(safeStock)

# 첫 번째 창 (재고 데이터를 입력하는 창)
class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow - test.ui")
        self.setGeometry(100, 100, 400, 200)

        # 재고데이터 입력 창
        self.label_1 = QLabel("재고데이터.csv:", self)
        self.label_1.move(20, 20)

        self.lineEdit_1 = QLineEdit(self)
        self.lineEdit_1.setGeometry(130, 20, 200, 20)

        self.file_button_1 = QPushButton("...", self)
        self.file_button_1.setGeometry(340, 20, 30, 20)
        self.file_button_1.clicked.connect(self.openFile1)

        # 월별데이터 입력 창
        self.label_2 = QLabel("월별데이터.csv:", self)
        self.label_2.move(20, 60)

        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.setGeometry(130, 60, 200, 20)

        self.file_button_2 = QPushButton("...", self)
        self.file_button_2.setGeometry(340, 60, 30, 20)
        self.file_button_2.clicked.connect(self.openFile2)

        # 예 버튼
        self.btn_1 = QPushButton("예(Y)", self)
        self.btn_1.setGeometry(100, 120, 80, 30)
        self.btn_1.clicked.connect(self.button1Function)

        # 아니오 버튼
        self.btn_2 = QPushButton("아니오(N)", self)
        self.btn_2.setGeometry(220, 120, 80, 30)
        self.btn_2.clicked.connect(self.button2Function)

    # btn_1이 눌리면 작동할 함수 (재고 데이터 및 판매 예측 실행)
    def button1Function(self):
        inventory_path = self.lineEdit_1.text()
        monthly_path = self.lineEdit_2.text()

        if not inventory_path or not monthly_path:
            QMessageBox.warning(self, "파일 오류", "모든 파일을 선택해주세요.")
            return

        inventory_df = pd.read_csv(inventory_path, encoding='cp949')
        monthly_df = pd.read_csv(monthly_path, encoding='cp949')

        monthly_df.columns = monthly_df.columns.str.strip().str.lower()
        inventory_df.columns = [
            'item', 'incomingStock', 'outcomingStock', 'currentStock', 
            'incomingDate', 'currentoutcomingDate', 'leadTime', 
            'predictedSale', 'expectedUsage', 'stdDev', 
            'safeStock', 'totalRequiredStock', 'serviceLevel'
        ]
        inventory_df['item'] = inventory_df['item'].str.strip().str.lower()

        for index, row in inventory_df.iterrows():
            itemName = row['item']
            if itemName in monthly_df.columns:
                monthlyData = monthly_df[itemName]
                predictedSale = predict_sale_for_item(monthlyData)
                inventory_df.at[index, 'predictedSale'] = round(predictedSale)

                safeStock = Safetystock(predictedSale, row['leadTime'], row['stdDev'], row['serviceLevel'])
                inventory_df.at[index, 'safeStock'] = safeStock

                expectedUsage = predictedSale * row['leadTime']
                inventory_df.at[index, 'expectedUsage'] = round(expectedUsage)

                totalRequiredStock = expectedUsage + safeStock
                inventory_df.at[index, 'totalRequiredStock'] = totalRequiredStock

        self.secondWindow = SecondWindow(inventory_df, self)
        self.secondWindow.show()

    # btn_2가 눌리면 작동할 함수 (창 종료)
    def button2Function(self):
        QCoreApplication.instance().quit()

    # 파일 선택 창 열기 함수
    def openFile1(self):
        fname, _ = QFileDialog.getOpenFileName(self, '파일 선택', '', 'CSV files (*.csv);;All Files (*)')
        if fname:
            self.lineEdit_1.setText(fname)

    def openFile2(self):
        fname, _ = QFileDialog.getOpenFileName(self, '파일 선택', '', 'CSV files (*.csv);;All Files (*)')
        if fname:
            self.lineEdit_2.setText(fname)

# 두 번째 창 (계산된 데이터를 출력하는 창)
class SecondWindow(QWidget):
    def __init__(self, inventory_df, main_window):
        super().__init__()
        self.setWindowTitle("Invento Memory")
        self.setGeometry(100, 100, 500, 400)
        self.inventory_df = inventory_df
        self.main_window = main_window

        layout = QVBoxLayout()
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        for index, row in inventory_df.iterrows():
            item_layout = QHBoxLayout()

            labels = [
                QLabel("재고명: "), QLabel("한달 평균 판매량: "), 
                QLabel("안전 재고 수량: "), QLabel("예상 사용량: "), 
                QLabel("총 필요 재고량: ")
            ]
            
            line_edits = [
                QLineEdit(str(row['item'])), QLineEdit(str(int(row['predictedSale']))),
                QLineEdit(str(int(row['safeStock']))), QLineEdit(str(int(row['expectedUsage']))),
                QLineEdit(str(int(row['totalRequiredStock'])))
            ]
            for edit in line_edits:
                edit.setReadOnly(True)

            for label, line_edit in zip(labels, line_edits):
                item_layout.addWidget(label)
                item_layout.addWidget(line_edit)

            scroll_layout.addLayout(item_layout)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        
    # 창이 닫힐 때 실행되는 이벤트 처리
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '파일 저장 확인', '파일로 저장하시겠습니까?', 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            save_path, _ = QFileDialog.getSaveFileName(self, "파일 저장", "", "CSV Files (*.csv);;All Files (*)")
            if save_path:
                self.inventory_df.to_csv(save_path, index=False, encoding='utf-8-sig')
        
        # 첫 번째 창도 함께 종료
        self.main_window.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())



