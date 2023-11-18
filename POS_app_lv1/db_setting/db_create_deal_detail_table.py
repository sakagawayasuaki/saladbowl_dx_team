import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
import csv

# Obtain connection string information from the portal
# 環境変数の読み込み
load_dotenv("../.env")
HOST = os.environ.get("HOST_NAME")
USN = os.environ.get("USER_NAME")
PWD = os.environ.get("PASSWORD")
DSN = os.environ.get("DB_NAME")
config = {
  'host':HOST,
  'user':USN,
  'password':PWD,
  'database':'customer_db'
}

# Construct connection string

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

# 顧客データ追加
with open('../../../取引明細_ダミーデータ.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダ行をスキップ

    for row in reader:
        trd_id = row[0]
        dtl_id = row[1]
        prd_id = row[2]
        prd_code = row[3]
        prd_name = row[4]
        prd_price = row[5]
        tax_cd = row[6]

        # データを取引詳細テーブルに挿入
        cursor.execute('''
          INSERT INTO deal_detail3 (trd_id, dtl_id, prd_id, prd_code, prd_name, prd_price, tax_cd)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (trd_id, dtl_id, prd_id, prd_code, prd_name, prd_price, tax_cd))

# トランザクションをコミット
conn.commit()

# Cleanup
cursor.close()
conn.close()
print("Done.")