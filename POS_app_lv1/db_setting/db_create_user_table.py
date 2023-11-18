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
with open('../../../ショップ_顧客マスタ_ダミーデータ.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダ行をスキップ

    for row in reader:
        usr_id = row[0]
        usr_name = row[1]
        usr_mail = row[2]
        usr_pw = row[3]

        # データをテーブルに挿入
        cursor.execute('''
          INSERT INTO user3 (usr_id, usr_name, usr_mail, usr_pw)
          VALUES (%s, %s, %s, %s)
        ''', (usr_id, usr_name, usr_mail, usr_pw))

# トランザクションをコミット
conn.commit()

# Cleanup
cursor.close()
conn.close()
print("Done.")