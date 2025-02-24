// Initialize Stripe
let stripe;
let elements;

document.addEventListener('DOMContentLoaded', async function() {
    displayCart();
    
    // Get Stripe publishable key
    const response = await fetch('/config');
    const { publishableKey } = await response.json();
    stripe = Stripe(publishableKey);

    // Create payment element
    const appearance = {
        theme: 'night',
        variables: {
            colorPrimary: '#33ff00',
            colorBackground: '#1a1a1a',
            colorText: '#33ff00',
            colorDanger: '#ff3864',
            fontFamily: '"Press Start 2P", cursive',
        },
    };
    
    elements = stripe.elements({ appearance });
    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element');
});

function displayCart() {
    const cart = JSON.parse(localStorage.getItem('cart'));
    const cartItems = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');
    const emptyCartMessage = document.getElementById('empty-cart-message');
    
    if (cart.length === 0) {
        cartItems.style.display = 'none';
        cartSummary.style.display = 'none';
        emptyCartMessage.style.display = 'block';
        return;
    }
    
    cartItems.style.display = 'block';
    cartSummary.style.display = 'block';
    emptyCartMessage.style.display = 'none';
    
    // Clear existing items
    cartItems.innerHTML = '';
    
    // Create cart items HTML
    cart.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'card mb-3';
        itemElement.innerHTML = `
            <div class="card-body">
                <div class="row">
                    <div class="col-md-2">
                        <img src="https://via.placeholder.com/100" alt="Product Image" class="img-fluid">
                    </div>
                    <div class="col-md-4">
                        <h5 class="card-title">Product ${item.productId}</h5>
                        <p class="card-text">Quantity: ${item.quantity}</p>
                    </div>
                    <div class="col-md-3">
                        <button class="btn btn-sm btn-danger" onclick="removeFromCart('${item.productId}')">Remove</button>
                    </div>
                </div>
            </div>
        `;
        cartItems.appendChild(itemElement);
    });
    
    // Update total
    updateCartTotal();
}

function removeFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart'));
    cart = cart.filter(item => item.productId !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCart();
    updateCartCount();
}

function updateCartTotal() {
    // This is a placeholder - in a real application, you would calculate this based on actual product prices
    const cart = JSON.parse(localStorage.getItem('cart'));
    const total = cart.reduce((sum, item) => sum + (item.quantity * 19.99), 0);
    document.getElementById('cart-total').textContent = total.toFixed(2);
}

// Handle payment form submission
const paymentForm = document.getElementById('payment-form');
if (paymentForm) {
    paymentForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const submitButton = document.getElementById('submit-payment');
        const spinner = document.getElementById('spinner');
        const buttonText = document.getElementById('button-text');
        const messageContainer = document.getElementById('payment-message');
        
        // Clear any previous error messages
        messageContainer.textContent = '';
        
        // Disable the submit button and show spinner
        submitButton.disabled = true;
        spinner.style.display = 'inline-block';
        buttonText.style.display = 'none';
        
        try {
            // Create payment intent
            const cart = JSON.parse(localStorage.getItem('cart')) || [];
            const response = await fetch('/api/create-payment-intent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    items: cart
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to create payment intent');
            }
            
            const { clientSecret } = await response.json();
            
            // Confirm the payment
            const { error } = await stripe.confirmPayment({
                elements,
                confirmParams: {
                    return_url: window.location.origin + '/order-confirmation'
                }
            });
            
            if (error) {
                messageContainer.textContent = error.message;
            }
            
        } catch (error) {
            messageContainer.textContent = 'An error occurred while processing your payment.';
            console.error('Payment error:', error);
        }
        
        // Re-enable the submit button and hide spinner
        submitButton.disabled = false;
        spinner.style.display = 'none';
        buttonText.style.display = 'inline-block';
    });
}

// Handle error messages
function showError(message) {
    const messageContainer = document.getElementById('payment-message');
    messageContainer.textContent = message;
    messageContainer.style.display = 'block';
    setTimeout(() => {
        messageContainer.style.display = 'none';
    }, 4000);
}
