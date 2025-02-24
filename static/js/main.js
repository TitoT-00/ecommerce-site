// Initialize cart in localStorage if it doesn't exist
if (!localStorage.getItem('cart')) {
    localStorage.setItem('cart', JSON.stringify([]));
}

// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Update cart count on page load
    updateCartCount();

    // Add to cart button click handler
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const card = this.closest('.card');
            
            if (!card) {
                console.error('Could not find product card');
                return;
            }

            try {
                const product = {
                    id: productId,
                    name: card.querySelector('.card-title').textContent.trim(),
                    price: parseFloat(card.querySelector('.price').textContent.replace('$', '').trim()),
                    image_url: card.querySelector('img').src,
                    quantity: 1,
                    description: card.querySelector('.card-text').textContent.trim()
                };

                // Add platform/condition/compatibility if present
                const platformTag = card.querySelector('.platform-tag');
                if (platformTag) {
                    product.platform = platformTag.textContent.replace('Platform: ', '').trim();
                }

                const conditionTag = card.querySelector('.condition-tag');
                if (conditionTag) {
                    product.condition = conditionTag.textContent.replace('Condition: ', '').trim();
                }

                const compatibilityTag = card.querySelector('.compatibility-tag');
                if (compatibilityTag) {
                    product.compatibility = compatibilityTag.textContent.replace('For: ', '').trim();
                }

                addToCart(product);
                
                // Show success message
                const toast = document.createElement('div');
                toast.className = 'toast-message';
                toast.textContent = 'Added to cart!';
                document.body.appendChild(toast);
                
                setTimeout(() => {
                    toast.remove();
                }, 2000);
                
            } catch (error) {
                console.error('Error adding to cart:', error);
            }
        });
    });
});

function addToCart(product) {
    try {
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        console.log('Current cart:', cart); // Debug log
        
        // Check if product already exists in cart
        const existingProductIndex = cart.findIndex(item => item.id === product.id);
        
        if (existingProductIndex > -1) {
            // Increment quantity if product exists
            cart[existingProductIndex].quantity += 1;
        } else {
            // Add new product if it doesn't exist
            cart.push(product);
        }
        
        console.log('Updated cart:', cart); // Debug log
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
    } catch (error) {
        console.error('Error in addToCart:', error);
        throw error;
    }
}

function updateCartCount() {
    try {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = totalItems;
        }
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

// Clear cart for testing (comment out in production)
// localStorage.removeItem('cart');
