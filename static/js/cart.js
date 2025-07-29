document.addEventListener('DOMContentLoaded', () => {
  const cartItemsDiv = document.getElementById('cart-items');
  const cartTotalSpan = document.getElementById('cart-total');
  let cart = JSON.parse(localStorage.getItem('cart')) || [];

  if (cart.length === 0) {
    cartItemsDiv.innerHTML = '<p>Your cart is empty.</p>';
    cartTotalSpan.textContent = '0.00';
    return;
  }

  fetch('/products/search')
    .then(response => response.json())
    .then(products => {
      let total = 0;
      cartItemsDiv.innerHTML = '';
      cart.forEach(item => {
        const product = products.find(p => p.id === item.id);
        if (product) {
          const itemDiv = document.createElement('div');
          itemDiv.classList.add('cart-item');
          itemDiv.innerHTML = `
            <span>${product.name}</span>
            <div>
              <input type="number" value="${item.quantity}" min="1" onchange="updateQuantity(${product.id}, this.value)">
              <span>$${ (product.price * item.quantity).toFixed(2) }</span>
              <button onclick="removeFromCart(${product.id})">Remove</button>
            </div>
          `;
          cartItemsDiv.appendChild(itemDiv);
          total += product.price * item.quantity;
        }
      });
      cartTotalSpan.textContent = total.toFixed(2);
    });
});

function updateQuantity(productId, quantity) {
  let cart = JSON.parse(localStorage.getItem('cart')) || [];
  const product = cart.find(item => item.id === productId);
  if (product) {
    product.quantity = parseInt(quantity) || 1;
    localStorage.setItem('cart', JSON.stringify(cart));
    location.reload();
  }
}

function removeFromCart(productId) {
  let cart = JSON.parse(localStorage.getItem('cart')) || [];
  cart = cart.filter(item => item.id !== productId);
  localStorage.setItem('cart', JSON.stringify(cart));
  location.reload();
}