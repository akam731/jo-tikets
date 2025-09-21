// Ticket Detail JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Auto-refresh QR code if not available (only once)
    const qrImage = document.querySelector('.qr-img img');
    if (!qrImage || !qrImage.src) {
        if (!sessionStorage.getItem('qr_refresh_attempted')) {
            sessionStorage.setItem('qr_refresh_attempted', 'true');
            setTimeout(() => {
                location.reload();
            }, 3000);
        }
    }
});

// Fonction pour copier la clé secrète
function copyKey() {
    const keyElement = document.getElementById('secretKey');
    const keyText = keyElement.textContent;
    
    // Utiliser l'API Clipboard si disponible
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(keyText).then(() => {
            showCopySuccess();
        }).catch(() => {
            fallbackCopy(keyText);
        });
    } else {
        fallbackCopy(keyText);
    }
}

// Méthode de fallback pour les navigateurs plus anciens
function fallbackCopy(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess();
    } catch (err) {
        showCopyError();
    }
    
    document.body.removeChild(textArea);
}

// Afficher le message de succès
function showCopySuccess() {
    const button = event.target.closest('button');
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fa-solid fa-check mr-1"></i>Copié !';
    button.classList.remove('bg-blue-500', 'hover:bg-blue-600');
    button.classList.add('bg-green-500');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('bg-green-500');
        button.classList.add('bg-blue-500', 'hover:bg-blue-600');
    }, 2000);
}

// Afficher le message d'erreur
function showCopyError() {
    const button = event.target.closest('button');
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fa-solid fa-times mr-1"></i>Erreur';
    button.classList.remove('bg-blue-500', 'hover:bg-blue-600');
    button.classList.add('bg-red-500');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('bg-red-500');
        button.classList.add('bg-blue-500', 'hover:bg-blue-600');
    }, 2000);
}
