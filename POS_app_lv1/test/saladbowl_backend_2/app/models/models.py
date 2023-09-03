#DBモデルを保存し、DB構造を確認
from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
# class Transaction(Base):
#     __tablename__ = "transactions"

#     trd_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     datetime = Column(TIMESTAMP, index=True)
#     emp_cd = Column(String(10), nullable=True)
#     store_cd = Column(String(5), nullable=False, default="30")
#     pos_no = Column(String(3), nullable=False, default="90")
#     total_amt = Column(Integer, default=0)

#     # リレーションシップ定義: 取引明細への参照
#     details = relationship("TransactionDetail", backref="transaction")

# # #取引明細テーブル
# class TransactionDetail(Base):
#     __tablename__ = "transaction_details"

#     trd_id = Column(Integer, ForeignKey('transactions.TRD_ID'), primary_key=True)
#     dtl_id = Column(Integer, primary_key=True, autoincrement=True)
#     prd_id = Column(Integer, ForeignKey('products.PRD_ID'))
#     prd_code = Column(String(13))
#     prd_name = Column(String(50))
#     prd_price = Column(Integer)

#     # リレーションシップ定義: 商品マスタとの参照
#     product = relationship("Product", backref="transaction_details")

