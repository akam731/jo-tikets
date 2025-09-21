"""
Context processors for the cart app.

Projet étudiant - BTS SIO
Date : Septembre 2024

J'ai créé ce context processor pour ajouter automatiquement
les informations du panier à tous les templates.
C'est plus pratique que de le faire dans chaque vue !
"""

from .models import Cart


def cart_context(request):
    """
    Ajoute les informations du panier au contexte de tous les templates.

    Si l'utilisateur est connecté, récupère son panier et calcule
    le nombre total d'articles et le prix total.
    """
    context = {
        "cart_items_count": 0,
        "cart_total_price": 0,
    }

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            context["cart_items_count"] = cart.total_items
            context["cart_total_price"] = float(cart.total_price)
        except Cart.DoesNotExist:
            # Le panier sera créé automatiquement lors du premier ajout
            pass

    return context
