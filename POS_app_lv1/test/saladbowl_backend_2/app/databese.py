from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
# 環境変数の読み込み
load_dotenv("../../../.env")
HOST = os.environ.get("HOST_NAME") #ホスト名
USN = os.environ.get("USER_NAME") #ユーザー名
PWD = os.environ.get("PASSWORD") #パスワード
DSN = os.environ.get("DB_NAME") #データベース名(product)
DATABASE_URL = f'mysql+mysqlconnector://{USN}:{PWD}@{HOST}/{DSN}'

# engineの設定
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()