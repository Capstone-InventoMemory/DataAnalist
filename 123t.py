import mysql.connector
from mysql.connector import Error

# 데이터베이스 연결 함수
def CreateConnection():
    try:
        db_connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        if db_connection.is_connected():
            print("데이터베이스 연결 성공")
            return db_connection
    except Error as err:
        print(f"Error: {err}")
        return None

# 오류 처리 함수
def HandleError(err):
    print(f"Error: {err}")

# 제품 데이터 삽입 함수
def InsertProductData(name, quantity, price):
    db_connection = CreateConnection()
    if db_connection is None:
        print("데이터베이스 연결 없음")
        return
   
    try:
        with db_connection.cursor() as cursor:
            sql = "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)"
            values = (name, quantity, price)
            cursor.execute(sql, values)
            db_connection.commit()
            print(f"Inserted {cursor.rowcount} record(s) into products.")
    except Error as err:
        HandleError(err)
    finally:
        db_connection.close()

# 제품 데이터 조회 함수
def FetchAllProducts():
    db_connection = CreateConnection()
    if db_connection is None:
        print("데이터베이스 연결 없음")
        return
   
    try:
        with db_connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                print(row)
    except Error as err:
        HandleError(err)
    finally:
        db_connection.close()

# 예시 데이터값 삽입
# InsertProductData("Sample Product", 100, 29.99)

FetchAllProducts()
