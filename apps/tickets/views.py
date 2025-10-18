"""
Views for the tickets app.
"""

import json
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Ticket


@login_required
def my_tickets_view(request):
    """
    View to display user's tickets.
    """
    tickets = Ticket.objects.filter(user=request.user).order_by("-created_at")
    # Regénère l'image si elle est manquante sur le disque (ex: prod après redeploy)
    for t in tickets:
        try:
            file_missing = not t.qr_image or not default_storage.exists(t.qr_image.name)
        except Exception:
            file_missing = True
        if file_missing and t.final_key:
            t.qr_image.delete(save=False)
            t.qr_image = None
            t.generate_qr_code()
    return render(request, "tickets/my_tickets.html", {"tickets": tickets})


@login_required
def ticket_detail_view(request, ticket_id):
    """
    View to display a specific ticket.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    # Force QR code generation if missing (fichier absent sur disque)
    try:
        file_missing = not ticket.qr_image or not default_storage.exists(ticket.qr_image.name)
    except Exception:
        file_missing = True
    if file_missing and ticket.final_key:
        ticket.qr_image.delete(save=False)
        ticket.qr_image = None
        ticket.generate_qr_code()

    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


@csrf_exempt
@require_http_methods(["POST"])
def validate_ticket_api(request):
    """
    API endpoint to validate a ticket by QR code.

    POST /api/tickets/validate/
    Body: {"final_key": "abc123..."}
    """
    try:
        data = json.loads(request.body)
        final_key = data.get("final_key")

        if not final_key:
            return JsonResponse(
                {"success": False, "error": "final_key is required"}, status=400
            )

        # Validate ticket
        # D'abord essayer de valider le billet (marquer comme utilisé si valide)
        is_valid, ticket, message = Ticket.validate_ticket(final_key)

        if is_valid:
            # Billet valide et marqué comme utilisé
            return JsonResponse(
                {
                    "success": True,
                    "ticket_id": ticket.id,
                    "user_name": ticket.user.get_full_name(),
                    "offer_name": ticket.order.offer.get_name_display(),
                    "purchase_date": ticket.created_at.isoformat(),
                    "status": ticket.status,
                    "message": message,
                }
            )
        else:
            # Si validation échouée, essayer de récupérer les infos quand même
            found, ticket, info_message = Ticket.get_ticket_info(final_key)

            if found and ticket:
                # Retourner erreur mais avec les infos du billet
                return JsonResponse(
                    {
                        "success": False,
                        "error": message,
                        "ticket_info": {
                            "ticket_id": ticket.id,
                            "user_name": ticket.user.get_full_name(),
                            "offer_name": ticket.order.offer.get_name_display(),
                            "purchase_date": ticket.created_at.isoformat(),
                            "status": ticket.status,
                        },
                    },
                    status=400,
                )
            else:
                return JsonResponse({"success": False, "error": message}, status=400)

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data"}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
