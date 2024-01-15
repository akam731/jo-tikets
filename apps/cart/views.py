"""
Views for the cart app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Cart, CartItem
from apps.catalog.models import Offer


@login_required
def cart_view(request):
    """
    Display the shopping cart.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {"cart": cart, "title": "Mon Panier"}
    return render(request, "cart/cart.html", context)


@login_required
@require_POST
def add_to_cart(request):
    """
    Add an offer to the cart.
    """
    try:
        data = json.loads(request.body)
        offer_id = data.get("offer_id")
        quantity = int(data.get("quantity", 1))

        offer = get_object_or_404(Offer, id=offer_id, is_active=True)
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if this offer already exists in the cart
        try:
            cart_item = CartItem.objects.get(cart=cart, offer=offer)
            # If it exists, increment the quantity
            cart_item.quantity += quantity
            cart_item.save()
            message = f"Quantité de l'offre {offer.get_name_display()} mise à jour (+{quantity})"
        except CartItem.DoesNotExist:
            # If it doesn't exist, create a new item
            cart_item = CartItem.objects.create(
                cart=cart, offer=offer, quantity=quantity
            )
            message = f"Offre {offer.get_name_display()} ajoutée au panier"

        return JsonResponse(
            {
                "success": True,
                "message": message,
                "cart_total": cart.total_items,
                "cart_price": float(cart.total_price),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erreur: {str(e)}"})


@login_required
@require_POST
def update_cart_item(request, item_id):
    """
    Update quantity of a cart item.
    """
    try:
        data = json.loads(request.body)
        quantity = int(data.get("quantity", 1))

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if quantity <= 0:
            cart_item.delete()
            message = f"{cart_item.offer.name} retiré du panier"
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = f"Quantité de {cart_item.offer.name} mise à jour"

        cart = cart_item.cart
        return JsonResponse(
            {
                "success": True,
                "message": message,
                "cart_total": cart.total_items,
                "cart_price": float(cart.total_price),
                "item_total": float(cart_item.total_price) if quantity > 0 else 0,
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erreur: {str(e)}"})


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart.
    """
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        offer_name = cart_item.offer.name
        cart_item.delete()

        cart = Cart.objects.get(user=request.user)
        return JsonResponse(
            {
                "success": True,
                "message": f"{offer_name} retiré du panier",
                "cart_total": cart.total_items,
                "cart_price": float(cart.total_price),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erreur: {str(e)}"})


@login_required
def checkout_view(request):
    """
    Display checkout page with payment form.
    """
    cart = get_object_or_404(Cart, user=request.user)

    if cart.items.count() == 0:
        messages.warning(request, "Votre panier est vide.")
        return redirect("cart:cart")

    context = {"cart": cart, "title": "Finaliser la commande"}
    return render(request, "cart/checkout.html", context)


@login_required
@require_POST
def process_payment(request):
    """
    Process payment (mock implementation).
    """
    try:
        data = json.loads(request.body)
        payment_method = data.get("payment_method")
        card_number = data.get("card_number", "")

        cart = get_object_or_404(Cart, user=request.user)

        if cart.items.count() == 0:
            return JsonResponse({"success": False, "message": "Votre panier est vide."})

        # Mock payment validation
        if payment_method == "card":
            if not card_number or len(card_number.replace(" ", "")) < 16:
                return JsonResponse(
                    {"success": False, "message": "Numéro de carte invalide."}
                )
        elif payment_method == "paypal":
            # For PayPal, we don't need card validation
            pass
        else:
            return JsonResponse(
                {"success": False, "message": "Méthode de paiement invalide."}
            )

        # Simulate payment processing
        import time

        time.sleep(1)  # Simulate processing time

        # Create orders for each individual ticket (one per quantity)
        from apps.orders.models import Order
        from apps.tickets.models import Ticket

        orders = []
        tickets = []

        for item in cart.items.all():
            # Create one order per individual ticket
            for i in range(item.quantity):
                order = Order.objects.create(
                    user=request.user,
                    offer=item.offer,
                    status="paid",
                    amount=item.offer.price,  # Price per individual ticket
                )
                orders.append(order)

                # Create ticket immediately for each order
                ticket = Ticket.objects.create(
                    order=order,
                    user=order.user,
                    final_key=f"{order.user.key1}_{order.id}_{order.created_at.timestamp()}",
                )
                # Generate QR code
                ticket.generate_qr_code()
                tickets.append(ticket)

        # Clear the cart
        cart.items.all().delete()

        return JsonResponse(
            {
                "success": True,
                "message": f"Paiement effectué avec succès ! {len(orders)} billet(s) généré(s).",
                "orders": [order.id for order in orders],
                "redirect_url": "/mes-billets/" if orders else "/",
            }
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Erreur lors du paiement: {str(e)}"}
        )


@login_required
@require_POST
def update_quantity_ajax(request):
    """
    Update quantity of a cart item via AJAX.
    """
    try:
        data = json.loads(request.body)
        item_id = data.get("item_id")
        quantity = int(data.get("quantity", 1))

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if quantity <= 0:
            cart_item.delete()
            cart = Cart.objects.get(user=request.user)
            return JsonResponse(
                {
                    "success": True,
                    "total_items": cart.total_items,
                    "cart_total": float(cart.total_price),
                    "item_total": 0,
                }
            )
        else:
            cart_item.quantity = quantity
            cart_item.save()
            cart = cart_item.cart
            return JsonResponse(
                {
                    "success": True,
                    "total_items": cart.total_items,
                    "cart_total": float(cart.total_price),
                    "item_total": float(cart_item.total_price),
                }
            )

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erreur: {str(e)}"})


@login_required
@require_POST
def remove_item_ajax(request):
    """
    Remove an item from the cart via AJAX.
    """
    try:
        data = json.loads(request.body)
        item_id = data.get("item_id")

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()

        cart = Cart.objects.get(user=request.user)
        return JsonResponse(
            {
                "success": True,
                "total_items": cart.total_items,
                "cart_total": float(cart.total_price),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erreur: {str(e)}"})
