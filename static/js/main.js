function searchProducts() {
  const query = document.getElementById('search').value;
  const category = document.getElementById('category').value;
  fetch(/products/search?q=${encodeURIComponent(query)}&category=${category})
    .then(response => response.json())
    .then(products => {
      const productList = document.getElementById('product-list');
      productList.innerHTML = '';
      products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product');
        productDiv.innerHTML = `
          <img src="/static/${product.image}" alt="${product.name}">
          <h3>${product.name}</h3>
          <p>${product.description}</p>
          <p>Category: ${product.category_name}</p>
          <p>$${product.price.toFixed(2)}</p>
          <button onclick="addToCart(${product.id})">Add to Cart</button>
        `;
        productList.appendChild(productDiv);
      });
    });
}

function addToCart(productId) {
  let cart = JSON.parse(localStorage.getItem('cart')) || [];
  const product = cart.find(item => item.id === productId);
  if (product) {
    product.quantity += 1;
  } else {
    cart.push({ id: productId, quantity: 1 });
  }
  localStorage.setItem('cart', JSON.stringify(cart));
  alert('Added to cart!');
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('search').addEventListener('input', searchProducts);
  document.getElementById('category').addEventListener('change', searchProducts);
});