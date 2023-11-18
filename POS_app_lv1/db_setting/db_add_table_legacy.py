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
  CREATE TABLE user_tmp (
    usr_id INT,
    usr_name VARCHAR(50),
    usr_mail VARCHAR(255),
    usr_pw VARBINARY(64),
    usr_bd DATE,
    usr_gender INT,
    usr_created TIMESTAMP,
    PRIMARY KEY(usr_id)
  );
''')

print("Finished creating table.")


# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")