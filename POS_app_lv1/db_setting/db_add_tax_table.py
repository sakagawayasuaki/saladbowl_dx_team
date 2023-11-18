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
cursor.execute("DROP TABLE IF EXISTS tax_rates;")
print("Finished dropping table (if existed).")

# Create table
cursor.execute('''
  CREATE TABLE tax_rates (
    id INT AUTO_INCREMENT,
    code CHAR(2) UNIQUE,
    name VARCHAR(20),
    percent DECIMAL(3,2),
    PRIMARY KEY(id)
    );
''')
print("Finished creating table.")

# Insert some data into table
# 税テーブル作成
cursor.execute("INSERT INTO tax_rates (code, name, percent) VALUES (%s, %s, %s);", ( "10", "10%", 0.1))

print("Inserted",cursor.rowcount,"row(s) of data.")

print("Finished creating table.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")