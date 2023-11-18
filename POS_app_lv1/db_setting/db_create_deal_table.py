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
  'database':DSN
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
with open('../../../取引_ダミーデータ.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダ行をスキップ

    for row in reader:
        trd_id = row[0]
        usr_id = row[1]
        datetime = row[2]
        emp_cd = row[3]
        store_cd = row[4]
        pos_no = row[5]
        total_amt = row[6]
        ttl_amt_ex_tax = row[7]

        # データを取引テーブルに挿入
        cursor.execute('''
          INSERT INTO deal3 (trd_id, usr_id, datetime, emp_cd, store_cd, pos_no, total_amt, ttl_amt_ex_tax)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (trd_id, usr_id, datetime, emp_cd, store_cd, pos_no, total_amt, ttl_amt_ex_tax))

# トランザクションをコミット
conn.commit()

# Cleanup
cursor.close()
conn.close()
print("Done.")