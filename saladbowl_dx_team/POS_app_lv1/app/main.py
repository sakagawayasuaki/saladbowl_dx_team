from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import NoResultFound


#from database import SessionLocal, engine, Base
from database import crud_products, database
from models import models
from typing import List


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# CORSミドルウェアの設定
origins = [
    "http://localhost:3000",  # Reactがデフォルトで使用するポート
    "your-production-frontend-url.com",# 実際の運用時には、フロントエンドのデプロイ先のURLも追加する必要があります。
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



#テスト用
@app.get("/")
def read_root():
    return {"Code": "Success"}


#商品コードをクエリとして受け取り、該当の商品情報を返す
@app.get("/product/")
def search_product_by_code(code: str,db: Session = Depends(get_db)):
    product = crud_products.get_product_by_code(db, code)
    if not product:
        return None  
    return product

#購入情報の受け取りと購入処理の実行
@app.post("/purchase/")
def purchase(
    emp_cd: str,
    store_cd: str,
    pos_no: str,
    product_list: list[dict],
    db: Session = Depends(get_db)
):
    # 取引テーブルへの登録
    trd_id = crud_products.create_transaction(db, emp_cd, store_cd, pos_no)

    # 取引明細への登録
    for product in product_list:
        crud_products.create_transaction_detail(db, trd_id, product)

    # 合計の計算
    total_amount = crud_products.calculate_total_amount(db, trd_id)

    # 取引テーブルの更新
    crud_products.update_transaction(db, trd_id, total_amount["total_amount"])

    return {"success": True, "total_amount": total_amount["total_amount"]}


@app.get("/transaction/total_amount/{trd_id}")
def get_total_amount(trd_id: int, db: Session = Depends(get_db)):
    total = crud_products.calculate_total_amount(db, trd_id)
    if not total:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return total

