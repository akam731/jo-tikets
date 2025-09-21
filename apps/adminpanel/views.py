"""
Views for the adminpanel app.

This app provides a custom admin panel for managing offers and viewing sales statistics.
"""

import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Sum
from apps.catalog.models import Offer
from apps.orders.models import Order


def is_admin_panel_user(user):
    """
    Check if user has admin panel access.
    """
    return user.is_authenticated and user.is_adminpanel


@login_required
@user_passes_test(is_admin_panel_user)
def dashboard_view(request):
    """
    Admin dashboard with sales statistics.
    """
    # Get sales data by offer
    sales_data = (
        Order.objects.filter(status="paid")
        .values("offer__name")
        .annotate(count=Count("id"), total_amount=Sum("amount"))
        .order_by("offer__name")
    )

    # Calculate average price for each offer
    for item in sales_data:
        if item["count"] > 0:
            item["average_price"] = round(item["total_amount"] / item["count"], 2)
        else:
            item["average_price"] = 0

    # Prepare data for Chart.js
    chart_data = {
        "labels": [item["offer__name"] for item in sales_data],
        "datasets": [
            {
                "label": "Nombre de ventes",
                "data": [item["count"] for item in sales_data],
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.8)",
                    "rgba(54, 162, 235, 0.8)",
                    "rgba(255, 205, 86, 0.8)",
                ],
            }
        ],
    }

    # Get total statistics
    total_orders = Order.objects.filter(status="paid").count()
    total_revenue = (
        Order.objects.filter(status="paid").aggregate(total=Sum("amount"))["total"] or 0
    )

    # Get active offers count
    active_offers_count = Offer.objects.filter(is_active=True).count()

    context = {
        "title": "Tableau de Bord Administrateur",
        "chart_data": json.dumps(chart_data),
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "sales_data": sales_data,
        "active_offers_count": active_offers_count,
    }

    return render(request, "adminpanel/dashboard.html", context)


@login_required
@user_passes_test(is_admin_panel_user)
def offers_crud_view(request):
    """
    CRUD interface for offers management.
    """
    offers = Offer.objects.all().order_by("price")
    return render(
        request,
        "adminpanel/offers_crud.html",
        {"title": "Gestion des Offres", "offers": offers},
    )


@csrf_exempt
@require_http_methods(["GET"])
@login_required
@user_passes_test(is_admin_panel_user)
def offers_api(request):
    """
    API endpoint to get all offers.

    GET /api/admin/offers/
    """
    offers = Offer.objects.all().order_by("price")
    offers_data = []

    for offer in offers:
        offers_data.append(
            {
                "id": offer.id,
                "name": offer.name,
                "capacity": offer.capacity,
                "price": float(offer.price),
                "is_active": offer.is_active,
                "description": offer.description,
                "created_at": offer.created_at.isoformat(),
            }
        )

    return JsonResponse({"success": True, "offers": offers_data})


@csrf_exempt
@require_http_methods(["POST"])
@login_required
@user_passes_test(is_admin_panel_user)
def create_offer_api(request):
    """
    API endpoint to create a new offer.

    POST /api/admin/offers/
    """
    try:
        data = json.loads(request.body)

        offer = Offer.objects.create(
            name=data.get("name"),
            capacity=data.get("capacity"),
            price=data.get("price"),
            description=data.get("description", ""),
            is_active=data.get("is_active", True),
        )

        return JsonResponse(
            {
                "success": True,
                "offer": {
                    "id": offer.id,
                    "name": offer.name,
                    "capacity": offer.capacity,
                    "price": float(offer.price),
                    "is_active": offer.is_active,
                    "description": offer.description,
                },
                "message": "Offre créée avec succès",
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data"}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
@login_required
@user_passes_test(is_admin_panel_user)
def update_offer_api(request, offer_id):
    """
    API endpoint to update an offer.

    PUT /api/admin/offers/{id}/
    """
    try:
        offer = get_object_or_404(Offer, id=offer_id)
        data = json.loads(request.body)

        offer.name = data.get("name", offer.name)
        offer.capacity = data.get("capacity", offer.capacity)
        offer.price = data.get("price", offer.price)
        offer.description = data.get("description", offer.description)
        offer.is_active = data.get("is_active", offer.is_active)
        offer.save()

        return JsonResponse(
            {
                "success": True,
                "offer": {
                    "id": offer.id,
                    "name": offer.name,
                    "capacity": offer.capacity,
                    "price": float(offer.price),
                    "is_active": offer.is_active,
                    "description": offer.description,
                },
                "message": "Offre mise à jour avec succès",
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data"}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
@user_passes_test(is_admin_panel_user)
def delete_offer_api(request, offer_id):
    """
    API endpoint to delete an offer.

    DELETE /api/admin/offers/{id}/
    """
    try:
        offer = get_object_or_404(Offer, id=offer_id)
        offer_name = offer.name
        offer.delete()

        return JsonResponse(
            {"success": True, "message": f'Offre "{offer_name}" supprimée avec succès'}
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
