"""
Views for the orders app.
"""

import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Order
from apps.catalog.models import Offer


@login_required
def checkout_view(request):
    """
    Checkout page view.
    """
    return render(request, "orders/checkout.html")


@login_required
def confirmation_view(request, order_id):
    """
    Order confirmation page view.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Create ticket if order is paid and no ticket exists
    if order.status == "paid" and not hasattr(order, "ticket"):
        from apps.tickets.models import Ticket

        ticket = Ticket.objects.create(
            order=order,
            user=order.user,
            final_key=f"{order.user.key1}_{order.id}_{order.created_at.timestamp()}",
        )
        # Generate QR code
        ticket.generate_qr_code()

    return render(request, "orders/confirmation.html", {"order": order})


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_order_api(request):
    """
    API endpoint to create a new order.

    POST /api/orders/
    Body: {"offer_id": 1}
    """
    try:
        data = json.loads(request.body)
        offer_id = data.get("offer_id")

        if not offer_id:
            return JsonResponse(
                {"success": False, "error": "offer_id is required"}, status=400
            )

        offer = get_object_or_404(Offer, id=offer_id, is_active=True)

        # Check if user already has a pending order for this offer
        existing_order = Order.objects.filter(
            user=request.user, offer=offer, status="pending"
        ).first()

        if existing_order:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Vous avez déjà une commande en attente pour cette offre",
                },
                status=400,
            )

        # Create new order
        order = Order.objects.create(user=request.user, offer=offer, amount=offer.price)

        return JsonResponse(
            {
                "success": True,
                "order_id": order.id,
                "amount": float(order.amount),
                "offer_name": offer.get_name_display(),
                "message": "Commande créée avec succès",
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data"}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def mock_payment_api(request):
    """
    API endpoint for mock payment processing.

    POST /api/payments/mock/
    Body: {"order_id": 1, "payment_method": "card"}
    """
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")

        if not order_id:
            return JsonResponse(
                {"success": False, "error": "order_id is required"}, status=400
            )

        order = get_object_or_404(Order, id=order_id, user=request.user)

        if not order.can_be_paid():
            return JsonResponse(
                {"success": False, "error": "Cette commande ne peut pas être payée"},
                status=400,
            )

        # Simulate payment processing
        # In a real application, this would integrate with a payment service provider
        payment_success = True  # Mock: always successful

        if payment_success:
            with transaction.atomic():
                # Mark order as paid
                order.mark_as_paid()

                # Create ticket (this will be handled by the tickets app)
                from apps.tickets.models import Ticket

                ticket = Ticket.objects.create(order=order, user=order.user)

                return JsonResponse(
                    {
                        "success": True,
                        "order_id": order.id,
                        "ticket_id": ticket.id,
                        "final_key": ticket.final_key,
                        "qr_code_url": ticket.qr_image.url if ticket.qr_image else None,
                        "message": "Paiement effectué avec succès",
                    }
                )
        else:
            return JsonResponse(
                {"success": False, "error": "Paiement échoué"}, status=400
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data"}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
