import datetime
from pydantic import BaseModel, Field
from typing import List

class Product(BaseModel):
    # 商品ID、商品コード、商品名称、商品単価 
    prd_id: int
    prd_cd: str
    prd_name: str
    prd_price: int
    class Config:
        orm_mode = True

class ProductList(BaseModel):
    product_list: List[Product]
    class Config:
        orm_mode = True

# class Transaction(TransactionCreate):
#     booking_id: int
#     datatime: datetime.datetime
#     class Config:
#         orm_mode = True

class TransactionResult(BaseModel):
    # 成否、合計金額
    check: bool
    total_amount: int
    class Config:
        orm_mode = True
