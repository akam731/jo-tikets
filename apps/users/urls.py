"""
URL configuration for the users app.
"""

from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("inscription/", views.SignUpView.as_view(), name="signup"),
    path("connexion/", views.login_view, name="login"),
    path("deconnexion/", views.logout_view, name="logout"),
    path("profil/", views.profile_view, name="profile"),
    path("construction/", views.construction_view, name="construction"),
    path("a-propos/", views.construction_view, name="about"),
    path("contact/", views.construction_view, name="contact"),
    path("aide/", views.construction_view, name="help"),
    path("mentions-legales/", views.construction_view, name="legal"),
    path("cgv/", views.construction_view, name="terms"),
    path("politique-confidentialite/", views.construction_view, name="privacy"),
]
