#DB接続とセッション管理を行う
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from dotenv import load_dotenv

#load_dotenv("../../../.env")
#HOST = os.environ.get("HOST_NAME") #ホスト名
#USN = os.environ.get("USER_NAME") #ユーザー名
#PWD = os.environ.get("PASSWORD") #パスワード
#DSN = os.environ.get("DB_NAME") #データベース名(product)
#DATABASE_URL = f'mysql+mysqlconnector://{USN}:{PWD}@{HOST}/{DSN}'

DATABASE_URL = "mysql+mysqlconnector://Tech0class1to46:Step4-class1to4-6@mysql-class1to4-japaneast-6.mysql.database.azure.com/db_pos_lv1"

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


