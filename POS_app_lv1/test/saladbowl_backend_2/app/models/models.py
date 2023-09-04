#DBモデルを保存し、DB構造を確認
from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from datetime import datetime


Base = declarative_base()
# Base.query  = db_session.query_property()

#商品マスターテーブル
class Product(Base):
    __tablename__ = "product"

    prd_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prd_cd = Column(String(13), unique=True, index=True) 
    prd_name = Column(String(50), index=True)
    prd_price = Column(Integer)

#取引テーブル
class Transaction(Base):
    __tablename__ = "deal"

    trd_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    detetime = Column(TIMESTAMP,default=datetime.utcnow)
    emp_cd = Column(String(10), nullable=True, default="9999999999")
    store_cd = Column(String(5), nullable=False, default="30")
    pos_no = Column(String(3), nullable=False, default="90")
    total_amt = Column(Integer, default=0)

#     # リレーションシップ定義: 取引明細への参照
#     details = relationship("TransactionDetail", backref="transaction")

# # #取引明細テーブル
class TransactionDetail(Base):
    __tablename__ = "deal_detail"

    trd_id = Column(Integer, ForeignKey('deal.trd_id'), primary_key=True)
    dtl_id = Column(Integer, primary_key=True, autoincrement=True)
    prd_id = Column(Integer, ForeignKey('product.prd_id'))
    prd_code = Column(String(13))
    prd_name = Column(String(50))
    prd_price = Column(Integer)

#     # リレーションシップ定義: 商品マスタとの参照
#     product = relationship("Product", backref="transaction_details")

