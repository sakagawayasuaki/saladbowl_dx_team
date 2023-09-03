from fastapi import FastAPI, Depends, HTTPException
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import NoResultFound
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# import json

# from database import base_class #SessionLocal, engine, Base
# from models import products
# from routers import product_router, purchase_router
# from . import crud_products, models, database
# import crud_products
from models import models

app = FastAPI()

# models.Base.metadata.create_all(bind=database.engine)

# 環境変数の読み込み
load_dotenv("../../../.env")
HOST = os.environ.get("HOST_NAME") #ホスト名
USN = os.environ.get("USER_NAME") #ユーザー名
PWD = os.environ.get("PASSWORD") #パスワード
DSN = os.environ.get("DB_NAME") #データベース名(product)
DATABASE_URL = f'mysql+mysqlconnector://{USN}:{PWD}@{HOST}/{DSN}'
# engineの設定
engine = create_engine(DATABASE_URL)
# セッションの作成
db_session = scoped_session(
  sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
  )
)
# テーブルを作成する
# Base = declarative_base()
# Base.query  = db_session.query_property()

# # CORSミドルウェアの設定
# origins = [
#     "http://localhost:3000",  # Reactがデフォルトで使用するポート
#     "your-production-frontend-url.com",# 実際の運用時には、フロントエンドのデプロイ先のURLも追加する必要があります。
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(products.router, prefix="/products", tags=["products"])
# app.include_router(purchase.router, prefix="/purchase", tags=["purchase"])

#テスト用
@app.get("/")
def read_root():
    db = db_session.query(models.Product).all()
    code_list =[]
    for row in db:
    # カラムを指定してデータを取得する
        code_list.append(row.prd_cd)
    return {"code": code_list}

#商品コードをクエリとして受け取り、該当の商品情報を返す
@app.get("/product/")
def search_product_by_code(code: str):
    product = db_session.query(models.Product).filter(models.Product.prd_cd == code).first()
    return product
    # product = crud_products.get_product_by_code(db_session, code)
    # if not product:
    #     return None  
    

# #購入情報の受け取りと購入処理の実行
# @app.post("/purchase/")
# def purchase(
#     emp_cd: str,
#     store_cd: str,
#     pos_no: str,
#     product_list: list[dict],
#     db: Session = Depends(database.get_db)
# ):
#     # 取引テーブルへの登録
#     trd_id = crud_products.create_transaction(db, emp_cd, store_cd, pos_no)

#     # 取引明細への登録
#     for product in product_list:
#         crud_products.create_transaction_detail(db, trd_id, product)

#     # 合計の計算
#     total_amount = crud_products.calculate_total_amount(db, trd_id)

#     # 取引テーブルの更新
#     crud_products.update_transaction(db, trd_id, total_amount["total_amount"])

#     return {"success": True, "total_amount": total_amount["total_amount"]}


# @app.get("/transaction/total_amount/{trd_id}")
# def get_total_amount(trd_id: int, db: Session = Depends(database.get_db)):
#     total = crud_products.calculate_total_amount(db, trd_id)
#     if not total:
#         raise HTTPException(status_code=404, detail="Transaction not found")
#     return total


# #タスク
# ##エラーハンドリング