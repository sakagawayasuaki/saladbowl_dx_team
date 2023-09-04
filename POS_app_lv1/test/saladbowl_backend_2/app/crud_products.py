#DBのCRUD操作
from sqlalchemy.orm import Session
from models import models
from schemas import schemas
import datetime

# 商品の追加
# def create_product(db: Session, product: Product):
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     return product

# 商品コードによる商品の検索
def get_product_by_code(db: Session, code: str):
    product = db.query(models.Product).filter(models.Product.prd_cd == code).first()
    return product

# 取引テーブルの初回追加
def create_init_transaction(db: Session):
    transaction = models.Transaction()
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction.trd_id

# 取引明細の追加
def create_transaction_detail(db: Session, trd_id:int, product: schemas.Product):
    transaction_detail = models.TransactionDetail(
        trd_id = trd_id,
        prd_id = product.prd_id,
        prd_code = product.prd_cd,
        prd_name = product.prd_name,
        prd_price = product.prd_price
    )
    db.add(transaction_detail)
    db.commit()
    db.refresh(transaction_detail)
    return transaction_detail.prd_price

# 取引テーブルの合計金額を更新
def update_transaction(db: Session, trd_id:str, total_amt:int):
    # Update
    transaction = db.query(models.Transaction).filter(models.Transaction.trd_id==trd_id).first()
    try:
        transaction.total_amt = total_amt
        db.commit()
        return True
    except:
        return False

# # 取引に関する合計金額の計算
# def calculate_total_amount(db: Session, trd_id: int):
#     total = db.query(models.TransactionDetail.PRD_PRICE).filter(models.TransactionDetail.TRD_ID == trd_id).all()
#     total_amount = sum([price[0] for price in total])
#     return {"total_amount": total_amount}