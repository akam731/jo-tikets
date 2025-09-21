"""
Tests pour l'application users.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from apps.users.forms import CustomUserCreationForm, UserLoginForm

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for the User model."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpass123",
        }

    def test_user_creation(self):
        """Test user creation with required fields."""
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_employee)
        self.assertFalse(user.is_adminpanel)

    def test_key1_generation(self):
        """Test that key1 is automatically generated on user creation."""
        user = User.objects.create_user(**self.user_data)

        self.assertTrue(user.key1)
        self.assertEqual(len(user.key1), 43)  # token_urlsafe(32) produces 43 chars

    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.email} ({user.get_full_name()})"
        self.assertEqual(str(user), expected)

    def test_get_full_name(self):
        """Test get_full_name method."""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.first_name} {user.last_name}"
        self.assertEqual(user.get_full_name(), expected)

    def test_email_uniqueness(self):
        """Test that email must be unique."""
        User.objects.create_user(**self.user_data)

        with self.assertRaises(Exception):  # IntegrityError
            User.objects.create_user(
                email="test@example.com",
                username="testuser2",
                first_name="Test2",
                last_name="User2",
                password="testpass123",
            )

    def test_employee_user(self):
        """Test employee user creation."""
        user = User.objects.create_user(**self.user_data, is_employee=True)

        self.assertTrue(user.is_employee)

    def test_admin_panel_user(self):
        """Test admin panel user creation."""
        user = User.objects.create_user(**self.user_data, is_adminpanel=True)

        self.assertTrue(user.is_adminpanel)

    def test_superuser_creation(self):
        """Test superuser creation."""
        user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            first_name="Admin",
            last_name="User",
            password="adminpass123",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_adminpanel)


class UserSignalsTest(TestCase):
    """Test cases for user signals."""

    def test_key1_generation_signal(self):
        """Test that key1 is generated via post_save signal."""
        user = User(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        user.save()

        # Refresh from database
        user.refresh_from_db()
        self.assertTrue(user.key1)
        self.assertEqual(len(user.key1), 43)


class UserFormTest(TestCase):
    """Tests pour les formulaires d'utilisateur."""

    def setUp(self):
        """Configuration des données de test."""
        self.valid_data = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }

    def test_custom_user_creation_form_valid(self):
        """Test du formulaire de création d'utilisateur avec des données valides."""
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_email_required(self):
        """Test que l'email est requis."""
        data = self.valid_data.copy()
        data["email"] = ""
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_custom_user_creation_form_email_unique(self):
        """Test que l'email doit être unique."""
        # Créer un utilisateur existant
        User.objects.create_user(
            email="test@example.com",
            username="existing",
            first_name="Existing",
            last_name="User",
            password="testpass123",
        )

        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_custom_user_creation_form_password_mismatch(self):
        """Test que les mots de passe doivent correspondre."""
        data = self.valid_data.copy()
        data["password2"] = "DifferentPassword123!"
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_custom_user_creation_form_username_generation(self):
        """Test la génération automatique du nom d'utilisateur."""
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        expected_username = "dupont.jean"
        self.assertEqual(user.username, expected_username)

    def test_custom_user_creation_form_username_duplicate_handling(self):
        """Test la gestion des noms d'utilisateur en double."""
        # Créer un utilisateur existant avec le même nom
        User.objects.create_user(
            email="existing@example.com",
            username="dupont.jean",
            first_name="Existing",
            last_name="Dupont",
            password="testpass123",
        )

        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        expected_username = "dupont.jean1"
        self.assertEqual(user.username, expected_username)

    def test_custom_user_creation_form_username_cleanup(self):
        """Test le nettoyage des noms pour le nom d'utilisateur."""
        data = self.valid_data.copy()
        data["first_name"] = "Jean-Pierre"
        data["last_name"] = "Dupont-Martin"

        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()
        expected_username = "dupontmartin.jeanpierre"
        self.assertEqual(user.username, expected_username)

    def test_user_login_form_valid(self):
        """Test du formulaire de connexion avec des données valides."""
        form = UserLoginForm(
            data={"email": "test@example.com", "password": "testpass123"}
        )
        self.assertTrue(form.is_valid())

    def test_user_login_form_email_required(self):
        """Test que l'email est requis pour la connexion."""
        form = UserLoginForm(data={"password": "testpass123"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_user_login_form_password_required(self):
        """Test que le mot de passe est requis pour la connexion."""
        form = UserLoginForm(data={"email": "test@example.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)


class UserViewTest(TestCase):
    """Tests pour les vues d'utilisateur."""

    def setUp(self):
        """Configuration des données de test."""
        self.client = Client()
        self.signup_url = reverse("users:signup")
        self.login_url = reverse("users:login")
        self.home_url = reverse("users:home")

        self.valid_signup_data = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }

        self.valid_login_data = {
            "email": "test@example.com",
            "password": "MotDePasse123!",
        }

    def test_signup_view_get(self):
        """Test de l'affichage de la page d'inscription."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inscription")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_signup_view_post_valid(self):
        """Test de l'inscription avec des données valides."""
        response = self.client.post(self.signup_url, self.valid_signup_data)

        # Vérifier la redirection vers la page d'accueil
        self.assertRedirects(response, self.home_url)

        # Vérifier que l'utilisateur a été créé
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

        # Vérifier que l'utilisateur est connecté automatiquement
        user = User.objects.get(email="test@example.com")
        self.assertTrue(user.is_authenticated)

    def test_signup_view_post_invalid(self):
        """Test de l'inscription avec des données invalides."""
        data = self.valid_signup_data.copy()
        data["password2"] = "DifferentPassword123!"

        response = self.client.post(self.signup_url, data)

        # Vérifier que la page est réaffichée avec les erreurs
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Les deux mots de passe ne correspondent pas")

        # Vérifier que l'utilisateur n'a pas été créé
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_signup_view_duplicate_email(self):
        """Test de l'inscription avec un email déjà existant."""
        # Créer un utilisateur existant
        User.objects.create_user(
            email="test@example.com",
            username="existing",
            first_name="Existing",
            last_name="User",
            password="testpass123",
        )

        response = self.client.post(self.signup_url, self.valid_signup_data)

        # Vérifier que la page est réaffichée avec l'erreur
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Un compte avec cette adresse email existe déjà")

    def test_signup_view_username_generation(self):
        """Test la génération automatique du nom d'utilisateur lors de l'inscription."""
        self.client.post(self.signup_url, self.valid_signup_data)

        # Vérifier que l'utilisateur a été créé avec le bon nom d'utilisateur
        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.username, "dupont.jean")

    def test_signup_view_auto_login(self):
        """Test la connexion automatique après inscription."""
        self.client.post(self.signup_url, self.valid_signup_data)

        # Vérifier que l'utilisateur est connecté
        self.assertTrue(self.client.session.get('_auth_user_id'))

        # Vérifier le message de succès
        response = self.client.get('/')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Bienvenue" in str(message) for message in messages))

    def test_login_view_get(self):
        """Test de l'affichage de la page de connexion."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion")
        self.assertIsInstance(response.context["form"], UserLoginForm)

    def test_login_view_post_valid(self):
        """Test de la connexion avec des données valides."""
        # Créer un utilisateur
        User.objects.create_user(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="MotDePasse123!",
        )

        response = self.client.post(self.login_url, self.valid_login_data)

        # Vérifier la redirection vers la page d'accueil
        self.assertRedirects(response, self.home_url)

        # Vérifier que l'utilisateur est connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid(self):
        """Test de la connexion avec des données invalides."""
        data = self.valid_login_data.copy()
        data["password"] = "WrongPassword123!"

        response = self.client.post(self.login_url, data)

        # Vérifier que la page est réaffichée avec l'erreur
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email ou mot de passe incorrect")

    def test_login_view_nonexistent_user(self):
        """Test de la connexion avec un utilisateur inexistant."""
        response = self.client.post(self.login_url, self.valid_login_data)

        # Vérifier que la page est réaffichée avec l'erreur
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email ou mot de passe incorrect")

    def test_logout_view(self):
        """Test de la déconnexion."""
        # Créer et connecter un utilisateur
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="MotDePasse123!",
        )
        self.client.force_login(user)

        # Vérifier que l'utilisateur est connecté
        self.assertTrue(user.is_authenticated)

        # Se déconnecter
        logout_url = reverse("users:logout")
        response = self.client.post(logout_url)

        # Vérifier la redirection vers la page d'accueil
        self.assertRedirects(response, self.home_url)

        # Vérifier que l'utilisateur est déconnecté
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserPasswordValidationTest(TestCase):
    """Tests pour la validation des mots de passe."""

    def setUp(self):
        """Configuration des données de test."""
        self.client = Client()
        self.signup_url = reverse("users:signup")

    def test_password_too_short(self):
        """Test qu'un mot de passe trop court est rejeté."""
        data = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "1234567",  # 7 caractères seulement
            "password2": "1234567",
        }

        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce mot de passe est trop court")

    def test_password_too_similar_to_user_info(self):
        """Test qu'un mot de passe trop similaire aux informations utilisateur est rejeté."""
        data = {
            "email": "jean@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "jean123",  # Contient le prénom
            "password2": "jean123",
        }

        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        # Vérifier qu'il y a des erreurs de validation
        self.assertContains(response, "form-error")

    def test_password_entirely_numeric(self):
        """Test qu'un mot de passe entièrement numérique est rejeté."""
        data = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "12345678",  # Entièrement numérique
            "password2": "12345678",
        }

        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        # Vérifier qu'il y a des erreurs de validation
        self.assertContains(response, "form-error")

    def test_password_common_password(self):
        """Test qu'un mot de passe commun est rejeté."""
        data = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "password",  # Mot de passe commun
            "password2": "password",
        }

        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        # Vérifier qu'il y a des erreurs de validation
        self.assertContains(response, "form-error")

    def test_password_valid(self):
        """Test qu'un mot de passe valide est accepté."""
        data = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "Greggb9848e*",  # Mot de passe valide
            "password2": "Greggb9848e*",
        }

        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, reverse("users:home"))
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
