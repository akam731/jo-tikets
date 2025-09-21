"""
Formulaires pour l'application users.

Projet étudiant - BTS SIO
Date : Septembre 2024

J'ai créé ces formulaires personnalisés pour avoir un meilleur contrôle
sur la validation et l'affichage. C'est plus compliqué que les formulaires
par défaut mais ça donne un meilleur résultat !
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire de création d'utilisateur personnalisé qui utilise l'email comme identifiant principal.

    J'ai dû créer ce formulaire car Django utilise username par défaut
    et moi je veux utiliser l'email. C'est plus logique pour les utilisateurs !
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Votre adresse email",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full", "placeholder": "Prénom"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full", "placeholder": "Nom"}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style password fields
        self.fields["password1"].widget.attrs.update(
            {"class": "input input-bordered w-full", "placeholder": "Mot de passe"}
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "placeholder": "Confirmer le mot de passe",
            }
        )

    def clean_email(self):
        """
        S'assurer que l'email est unique.

        J'ai ajouté cette validation pour éviter les doublons d'emails.
        C'est important pour la sécurité !
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Un compte avec cette adresse email existe déjà."
            )
        return email

    def save(self, commit=True):
        """
        Sauvegarde l'utilisateur avec un nom d'utilisateur généré automatiquement.

        J'ai créé cette logique pour générer automatiquement un username
        au format Nom.Prenom. C'est plus pratique que de demander à l'utilisateur
        de choisir un nom d'utilisateur !
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        # Générer le nom d'utilisateur au format Nom.Prenom
        first_name = self.cleaned_data["first_name"].strip()
        last_name = self.cleaned_data["last_name"].strip()

        # Nettoyer les noms (enlever les espaces, caractères spéciaux)
        # J'ai appris cette technique sur Stack Overflow !
        first_name_clean = "".join(c for c in first_name if c.isalnum())
        last_name_clean = "".join(c for c in last_name if c.isalnum())

        # Créer le nom d'utilisateur de base
        base_username = f"{last_name_clean}.{first_name_clean}".lower()

        # Vérifier si le nom d'utilisateur existe déjà
        # Si oui, on ajoute un numéro (ex: martin.jean1, martin.jean2...)
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    Formulaire de connexion personnalisé.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Votre adresse email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Mot de passe",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # Supprimer 'request' des kwargs s'il est présent
        kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
