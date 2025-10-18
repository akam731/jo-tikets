"""
URL configuration for jo_tickets project.

Projet étudiant - BTS SIO
Date : Septembre 2024
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.conf.urls import handler400, handler403, handler404, handler500
from django.shortcuts import render


def health_check(request):
    return JsonResponse({"status": "ok", "message": "JO Tickets API is running"})


# Vue de test d'affichage des erreurs
def test_error_view(request, code):
    code_str = str(code).strip()
    if code_str.isdigit():
        status = int(code_str)
        if 400 <= status <= 599:
            messages = {
                400: "Requête invalide.",
                401: "Authentification requise.",
                403: "Accès refusé.",
                404: "Page non trouvée.",
                405: "Méthode non autorisée.",
                409: "Conflit de requête.",
                413: "Requête trop volumineuse.",
                415: "Type de média non supporté.",
                429: "Trop de requêtes.",
                500: "Erreur interne du serveur.",
                502: "Mauvaise passerelle.",
                503: "Service indisponible.",
                504: "Délai d'attente dépassé.",
            }
            message = messages.get(status, f"Erreur HTTP {status}")
            return error_view(request, status_code=status, message=message)

    return error_view(request, status_code=400, message=f"Code d'erreur inconnu: {code}")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("erreur/<str:code>/", test_error_view, name="test_error"),
    path("", include("apps.users.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.orders.urls")),
    path("", include("apps.tickets.urls")),
    path("", include("apps.adminpanel.urls")),
    path("", include("apps.control.urls")),
    path("", include("apps.cart.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Gestion des erreurs
def error_view(request, exception=None, status_code=500, message=None):
    context = {
        "status_code": status_code,
        "message": message,
    }
    return render(request, "errors/error.html", context, status=status_code)

handler400 = lambda request, exception=None: error_view(request, exception, 400, "Requête invalide.")
handler403 = lambda request, exception=None: error_view(request, exception, 403, "Accès refusé.")
handler404 = lambda request, exception=None: error_view(request, exception, 404, "Page non trouvée.")
handler500 = lambda request: error_view(request, None, 500, "Erreur interne du serveur.")