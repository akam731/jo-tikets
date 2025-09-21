// Offers JavaScript
function addToCart(offerId, offerName, price, capacity) {
    // Show loading state
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading loading-spinner loading-sm"></span> Ajout...';
    button.disabled = true;
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfToken) {
        showMessage('Erreur de sécurité. Veuillez recharger la page.', 'error');
        button.innerHTML = originalText;
        button.disabled = false;
        return;
    }
    
    // Add to cart
    fetch('/panier/ajouter/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken.value,
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        },
        body: JSON.stringify({
            offer_id: offerId,
            quantity: 1
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            // Update cart counter if it exists
            updateCartCounter(data.cart_total);
        } else {
            showMessage(data.message || 'Erreur lors de l\'ajout au panier', 'error');
        }
    })
    .catch(error => {
        showMessage('Erreur lors de l\'ajout au panier: ' + error.message, 'error');
    })
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

function updateCartCounter(count) {
    // Update desktop counter
    const cartCounter = document.getElementById('cart-counter');
    if (cartCounter) {
        cartCounter.textContent = count;
        cartCounter.classList.remove('hidden');
    }
    
    // Update mobile counter
    const cartCounterMobile = document.getElementById('cart-counter-mobile');
    if (cartCounterMobile) {
        cartCounterMobile.textContent = count;
        cartCounterMobile.classList.remove('hidden');
    }
}

function showMessage(message, type) {
    const toast = document.createElement('div');
    const isMobile = window.innerWidth <= 768;
    const width = isMobile ? '90%' : '80%';
    const minWidth = isMobile ? '280px' : '400px';
    const whiteSpace = isMobile ? 'normal' : 'nowrap';
    const fontSize = isMobile ? '0.9rem' : '1rem';
    
    toast.style.cssText = `position: fixed; top: 65px; left: 50%; transform: translateX(-50%); z-index: 1000; max-width: 90%; width: ${width}; min-width: ${minWidth}; white-space: ${whiteSpace};`;
    toast.innerHTML = `
        <div style="padding: ${isMobile ? '0.75rem 0.5rem' : '1rem'}; border-radius: 0.5rem; background: ${type === 'success' ? '#dcfce7' : '#fecaca'}; color: ${type === 'success' ? '#166534' : '#dc2626'}; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2); overflow: hidden; font-size: ${fontSize}; line-height: 1.4;">
            ${message}
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
