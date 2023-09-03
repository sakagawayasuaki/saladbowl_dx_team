from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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
import crud_products
from models import models
# from schemas import schemas
import databese


app = FastAPI()

models.Base.metadata.create_all(bind=databese.engine)

# Dependency
def get_db():
    db = databese.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#テスト用
@app.get("/")
def read_root():
    return {"code": "Success"}

#商品コードをクエリとして受け取り、該当の商品情報を返す
@app.get("/product/")
async def read_product_by_code(code: str,db: Session = Depends(get_db)):
    product = crud_products.get_product_by_code(db, code)
    return product
    

#購入情報の受け取りと購入処理の実行
# @app.post("/purchase/",response_model=schemas.Booking)
# def purchase(buy_data: schemas.TransactionCreate):
#     # 引数：レジ担当者コード、店舗コード、POS機ID、[商品一意キー,商品コード,商品名称,商品単価]のリスト

#     # 取引テーブルのモデル作成（取引キー、日時、レジ担当者コード、店舗コード、POSID、合計金額

#     # 取引テーブルへの登録（CREATE)
#     trd_id = crud_products.create_transaction(db, emp_cd, store_cd, pos_no)
    
#     # 取引明細テーブルのモデル作成（取引キー、取引明細キー、商品きー、商品コード、商品名称、商品単価

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