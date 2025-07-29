document.getElementById('checkout-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const cart = JSON.parse(localStorage.getItem('cart')) || [];
  fetch('/api/confirm-order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cart })
  })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      localStorage.removeItem('cart');
      window.location.href = '/';
    })
    .catch(error => alert('Error confirming order: ' + error));
});