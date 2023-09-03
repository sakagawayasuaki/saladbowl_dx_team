#DBのCRUD操作
from sqlalchemy.orm import Session
from models import models

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

# # 取引の追加
# def create_transaction(db: Session, transaction: models.Transaction):
#     db.add(transaction)
#     db.commit()
#     db.refresh(transaction)
#     return transaction

# # 取引明細の追加
# def create_transaction_detail(db: Session, transaction_detail: models.TransactionDetail):
#     db.add(transaction_detail)
#     db.commit()
#     db.refresh(transaction_detail)
#     return transaction_detail

# # 取引に関する合計金額の計算
# def calculate_total_amount(db: Session, trd_id: int):
#     total = db.query(models.TransactionDetail.PRD_PRICE).filter(models.TransactionDetail.TRD_ID == trd_id).all()
#     total_amount = sum([price[0] for price in total])
#     return {"total_amount": total_amount}