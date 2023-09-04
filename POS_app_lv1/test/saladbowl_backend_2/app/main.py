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
from fastapi.middleware.cors import CORSMiddleware
from typing import List
# import json

# from database import base_class #SessionLocal, engine, Base
# from models import products
# from routers import product_router, purchase_router
# from . import crud_products, models, database
import crud_products
from models import models
from schemas import schemas
import databese


app = FastAPI()

models.Base.metadata.create_all(bind=databese.engine)

# CORSミドルウェアの設定
origins = [
    "http://localhost:3002",  # Reactがデフォルトで使用するポート
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
@app.post("/purchase/",response_model=schemas.TransactionResult)
def purchase(products: List[schemas.Product], db: Session = Depends(get_db)):
    # 1-1：取引テーブルへの初期登録（CREATE)  戻り値：取引一意キー（trd_id）
    trd_id = crud_products.create_init_transaction(db=db)
    # 1-2：取引明細テーブルへの登録（繰り返し処理？）
    # 引数：取引キー、商品キー、商品コード、商品名称、商品単価
    # 戻り値：商品単価
    total_amount = 0
    for product in products:
        # 取引明細テーブルへの登録
        price = crud_products.create_transaction_detail(db=db, trd_id = trd_id, product=product)
        # 1-3：合計の計算
        total_amount += price

    # 1-4：取引テーブルの更新、戻り値：成否
    check = crud_products.update_transaction(db=db, trd_id = trd_id, total_amt=total_amount)
    if check == True:
        print(total_amount)
        return {"check": check, "total_amount": total_amount}
    else:
        return {"check": check, "total_amount": None}


# @app.get("/transaction/total_amount/{trd_id}")
# def get_total_amount(trd_id: int, db: Session = Depends(database.get_db)):
#     total = crud_products.calculate_total_amount(db, trd_id)
#     if not total:
#         raise HTTPException(status_code=404, detail="Transaction not found")
#     return total


# #タスク
# ##エラーハンドリング