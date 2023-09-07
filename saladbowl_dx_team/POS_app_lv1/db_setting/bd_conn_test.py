from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import os
from dotenv import load_dotenv

import pandas as pd

# 環境変数の読み込み
load_dotenv("../.env")
HOST = os.environ.get("HOST_NAME") #ホスト名
USN = os.environ.get("USER_NAME") #ユーザー名
PWD = os.environ.get("PASSWORD") #パスワード
DSN = os.environ.get("DB_NAME") #データベース名(product)

# engineの設定
engine = create_engine(f'mysql+mysqlconnector://{USN}:{PWD}@{HOST}/{DSN}')

# セッションの作成
db_session = scoped_session(
  sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
  )
)

# テーブルを作成する
Base = declarative_base()
Base.query  = db_session.query_property()

# テーブルを定義する
# Baseを継承
class Product(Base):
    __tablename__ = "product" #テーブル名修正 products → product

    prd_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prd_cd = Column(String(13), unique=True, index=True) #column名修正　prd_code →prd_cd
    prd_name = Column(String(50), index=True)
    prd_price = Column(Integer)


# DBにあるデータ(商品コード)を全件表示
db = db_session.query(Product).all()
for row in db:
  # カラムを指定してデータを取得する
  print(row.prd_cd)