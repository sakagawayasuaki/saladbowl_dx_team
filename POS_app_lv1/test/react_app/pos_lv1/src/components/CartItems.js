import React from 'react';
import './CartItems.css';


const CartItems = ({ cartItems , totalAmount }) => {

  // 商品コードごとに数量計算
  const aggregatedItems = {};
  cartItems.forEach((item) => {
    if (aggregatedItems[item.product]) {
      aggregatedItems[item.product].quantity += item.quantity;
    } else {
      aggregatedItems[item.product] = { ...item };
    }
  });


  return (
    <div className="Container_cartItems">

      {/* <div>
        <h5>合計金額（税込）: {totalAmount.toLocaleString()}円</h5>
      </div> */}

      {Object.values(aggregatedItems).map((item) => (
        <div key={item.id}>
          <p>{item.product}</p>
          <p>{item.price}円</p>
          <p>{item.quantity}個</p>
        </div>
      ))}
      

    </div>
  );
};

export default CartItems;