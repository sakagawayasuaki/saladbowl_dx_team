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

# 商品マスタ テーブル作成
# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS product;")
print("Finished dropping table (if existed).")

# Create table
cursor.execute('''
  CREATE TABLE product (
    prd_id INT AUTO_INCREMENT,
    prd_cd CHAR(13),
    prd_name VARCHAR(50),
    prd_price INT,
    PRIMARY KEY(prd_id)
    );
''')
print("Finished creating table.")

# Insert some data into table
cursor.execute("INSERT INTO product (prd_cd, prd_name, prd_price) VALUES (%s, %s, %s);", ("4902705090828","明治 LG21プロビオヨーグルト", 144))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO product (prd_cd, prd_name, prd_price) VALUES (%s, %s, %s);", ("4514603435016","ウィルキンソン ファイバー", 124))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO product (prd_cd, prd_name, prd_price) VALUES (%s, %s, %s);", ("4901301367402","花王 キュキュット ポンプ オレンジの香り", 198))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO product (prd_cd, prd_name, prd_price) VALUES (%s, %s, %s);", ("4901777201439","サントリー 角ハイボール350ml缶", 196))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO product (prd_cd, prd_name, prd_price) VALUES (%s, %s, %s);", ("4901411105147","キリン 一番搾り糖質ゼロ350ml缶", 203))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO product (prd_cd, prd_name, prd_price) VALUES (%s, %s, %s);", ("4902705090828","キリン 氷結®無糖 レモン350ml缶", 122))
print("Inserted",cursor.rowcount,"row(s) of data.")

# 取引 テーブル作成
# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS deal;")
print("Finished dropping table (if existed).")

# Create table
cursor.execute('''
  CREATE TABLE deal (
    trd_id INT AUTO_INCREMENT,
    datetime timestamp,
    emp_cd CHAR(10),
    store_cd CHAR(5),
    pos_no CHAR(3),
    total_amt INT,
    PRIMARY KEY(trd_id)
  );
''')
print("Finished creating table.")

# 取引明細 テーブル作成
# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS deal_dtail;")
print("Finished dropping table (if existed).")

# Create table
cursor.execute('''
  CREATE TABLE deal_dtail (
      trd_id INT,
      dtl_id INT,
      prd_id INT,
      prd_code CHAR(13),
      prd_name VARCHAR(50),
      prd_price INT,
      FOREIGN KEY (trd_id) REFERENCES deal(trd_id),
      FOREIGN KEY (prd_id) REFERENCES product(prd_id),
      PRIMARY KEY(trd_id, dtl_id)
  );
''')

print("Finished creating table.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")