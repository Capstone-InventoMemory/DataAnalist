import pandas as pd

monthly_df = pd.read_csv('Monthly_InventoryData.csv', encoding='cp949')
inventory_df = pd.read_csv('InventoryData.csv', encoding='cp949')

monthly_df.columns = monthly_df.columns.str.strip().str.lower() 
inventory_df.columns = [
    'item', 'incomingStock', 'outcomingStock', 'currentStock', 
    'incomingDate', 'currentoutcomingDate', 'leadTime', 
    'predictedSale', 'expectedUsage', 'stdDev', 
    'safeStock', 'totalRequiredStock', 'serviceLevel'
]
inventory_df['item'] = inventory_df['item'].str.strip().str.lower()  

##print("Monthly Data Columns:", monthly_df.columns.tolist())

def PredictSale(monthlyData):
    totalSales = monthlyData.sum() 
    daysInMonth = len(monthlyData) 
    return totalSales / daysInMonth if daysInMonth > 0 else 0 

for index, row in inventory_df.iterrows():
    itemName = row['item']
    
    if itemName in monthly_df.columns:
        monthlyData = monthly_df[itemName]  

        ##print(f"Processing item: {itemName}")
        ##print(f"Monthly data found: {monthlyData.values}")

        if monthlyData is not None and not monthlyData.empty:
        
            predictedSale = PredictSale(monthlyData.values)
            inventory_df.at[index, 'predictedSale'] = round(predictedSale)  
        else:
        
            inventory_df.at[index, 'predictedSale'] = 0

def ExpectedUsage(predictedSale, leadTime):
    return predictedSale * leadTime

inventory_df['expectedUsage'] = inventory_df.apply(
    lambda row: round(ExpectedUsage(row['predictedSale'], row['leadTime']), 1), axis=1 
)

inventory_df.to_csv('Updated_Predict_InventoryData.csv', index=False, encoding='cp949')

print(inventory_df[['item', 'predictedSale', 'expectedUsage']])