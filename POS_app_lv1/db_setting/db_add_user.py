import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

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


# 顧客テーブル追加
# Create table
cursor.execute('''
  CREATE TABLE user3 (
    usr_id INT,
    usr_name VARCHAR(50),
    usr_mail VARCHAR(255),
    usr_pw VARBINARY(64),
    PRIMARY KEY(usr_id)
  );
''')

# 取引テーブル追加
# Create table
cursor.execute('''
  CREATE TABLE deal3 (
    trd_id INT AUTO_INCREMENT,
    usr_id INT,
    datetime timestamp,
    emp_cd CHAR(10),
    store_cd CHAR(5),
    pos_no CHAR(3),
    total_amt INT,
    ttl_amt_ex_tax INT,
    FOREIGN KEY (usr_id) REFERENCES user3(usr_id),
    PRIMARY KEY(trd_id)
  );
''')
print("Finished creating table.")

# 取引明細 テーブル作成 
# Create table
cursor.execute('''
  CREATE TABLE deal_detail3 (
      trd_id INT,
      dtl_id INT AUTO_INCREMENT,
      prd_id INT,
      prd_code CHAR(13),
      prd_name VARCHAR(50),
      prd_price INT,
      tax_cd CHAR(2),
      FOREIGN KEY (trd_id) REFERENCES deal3(trd_id),
      FOREIGN KEY (prd_id) REFERENCES product(prd_id),
      PRIMARY KEY(dtl_id, trd_id)
  );
''')

print("Finished creating table.")


# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")