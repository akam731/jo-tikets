"""
Tests fonctionnels pour l'application users.

Ces tests simulent le comportement d'un utilisateur réel naviguant
dans l'application via un navigateur web.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

User = get_user_model()


class UserRegistrationFunctionalTest(TestCase):
    """Tests fonctionnels pour l'inscription d'utilisateur."""

    def setUp(self):
        """Configuration des données de test."""
        self.client = Client()
        self.signup_url = reverse("users:signup")
        self.home_url = reverse("users:home")
        self.login_url = reverse("users:login")

    def test_complete_registration_flow(self):
        """Test du flux complet d'inscription."""
        # 1. Accéder à la page d'inscription
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inscription")

        # 2. Remplir le formulaire d'inscription
        registration_data = {
            "email": "nouveau@example.com",
            "first_name": "Marie",
            "last_name": "Martin",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }

        # 3. Soumettre le formulaire
        response = self.client.post(self.signup_url, registration_data)

        # 4. Vérifier la redirection vers la page d'accueil
        self.assertRedirects(response, self.home_url)

        # 5. Vérifier que l'utilisateur a été créé
        self.assertTrue(User.objects.filter(email="nouveau@example.com").exists())
        user = User.objects.get(email="nouveau@example.com")
        self.assertEqual(user.first_name, "Marie")
        self.assertEqual(user.last_name, "Martin")
        self.assertEqual(user.username, "martin.marie")

        # 6. Vérifier que l'utilisateur est connecté automatiquement
        self.assertTrue(user.is_authenticated)

    def test_registration_with_invalid_data(self):
        """Test de l'inscription avec des données invalides."""
        # 1. Accéder à la page d'inscription
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

        # 2. Tenter l'inscription avec des mots de passe différents
        invalid_data = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "MotDePasse123!",
            "password2": "AutreMotDePasse456!",
        }

        # 3. Soumettre le formulaire
        response = self.client.post(self.signup_url, invalid_data)

        # 4. Vérifier que la page est réaffichée avec les erreurs
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Les deux mots de passe ne correspondent pas")

        # 5. Vérifier que l'utilisateur n'a pas été créé
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_registration_with_existing_email(self):
        """Test de l'inscription avec un email déjà existant."""
        # 1. Créer un utilisateur existant
        User.objects.create_user(
            email="existant@example.com",
            username="existant",
            first_name="Existant",
            last_name="User",
            password="testpass123",
        )

        # 2. Tenter l'inscription avec le même email
        duplicate_data = {
            "email": "existant@example.com",
            "first_name": "Nouveau",
            "last_name": "User",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }

        # 3. Soumettre le formulaire
        response = self.client.post(self.signup_url, duplicate_data)

        # 4. Vérifier que la page est réaffichée avec l'erreur
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Un compte avec cette adresse email existe déjà")

        # 5. Vérifier qu'aucun nouvel utilisateur n'a été créé
        self.assertEqual(User.objects.filter(email="existant@example.com").count(), 1)

    def test_registration_username_generation(self):
        """Test de la génération automatique du nom d'utilisateur."""
        # 1. Créer un utilisateur avec un nom spécifique
        User.objects.create_user(
            email="premier@example.com",
            username="martin.marie",
            first_name="Marie",
            last_name="Martin",
            password="testpass123",
        )

        # 2. Tenter l'inscription avec le même nom
        registration_data = {
            "email": "deuxieme@example.com",
            "first_name": "Marie",
            "last_name": "Martin",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }

        # 3. Soumettre le formulaire
        response = self.client.post(self.signup_url, registration_data)

        # 4. Vérifier la redirection
        self.assertRedirects(response, self.home_url)

        # 5. Vérifier que le nom d'utilisateur a été généré avec un numéro
        user = User.objects.get(email="deuxieme@example.com")
        self.assertEqual(user.username, "martin.marie1")

    def test_registration_form_validation(self):
        """Test de la validation des champs du formulaire."""
        # Test avec email manquant
        data_no_email = {
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }
        response = self.client.post(self.signup_url, data_no_email)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce champ est obligatoire")

        # Test avec prénom manquant
        data_no_first_name = {
            "email": "test@example.com",
            "last_name": "Dupont",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }
        response = self.client.post(self.signup_url, data_no_first_name)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce champ est obligatoire")

        # Test avec nom manquant
        data_no_last_name = {
            "email": "test@example.com",
            "first_name": "Jean",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }
        response = self.client.post(self.signup_url, data_no_last_name)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce champ est obligatoire")

    def test_registration_password_validation(self):
        """Test de la validation des mots de passe."""
        # Test avec mot de passe trop court
        data_short_password = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "1234567",  # 7 caractères seulement
            "password2": "1234567",
        }
        response = self.client.post(self.signup_url, data_short_password)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce mot de passe est trop court")

        # Test avec mot de passe entièrement numérique
        data_numeric_password = {
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(self.signup_url, data_numeric_password)
        self.assertEqual(response.status_code, 200)
        # Vérifier qu'il y a des erreurs de validation
        self.assertContains(response, "form-error")

    def test_registration_success_message(self):
        """Test du message de succès après inscription."""
        registration_data = {
            "email": "success@example.com",
            "first_name": "Success",
            "last_name": "User",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }

        response = self.client.post(self.signup_url, registration_data)

        # Vérifier le message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Bienvenue" in str(message) for message in messages))

    def test_registration_redirect_after_success(self):
        """Test de la redirection après inscription réussie."""
        registration_data = {
            "email": "redirect@example.com",
            "first_name": "Redirect",
            "last_name": "User",
            "password1": "MotDePasse123!",
            "password2": "MotDePasse123!",
        }

        response = self.client.post(self.signup_url, registration_data)

        # Vérifier la redirection vers la page d'accueil
        self.assertRedirects(response, self.home_url)

        # Vérifier que l'utilisateur peut accéder à la page d'accueil
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)


class UserRegistrationSeleniumTest(TestCase):
    """Tests fonctionnels avec Selenium pour simuler un navigateur réel.

    ATTENTION: Ces tests nécessitent que le serveur Django soit en cours d'exécution
    et que Chrome/ChromeDriver soit installé sur le système.
    """

    @classmethod
    def setUpClass(cls):
        """Configuration de Selenium."""
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode sans interface graphique
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            # Si Chrome n'est pas disponible, on skip les tests Selenium
            cls.driver = None
            print(f"Selenium WebDriver non disponible: {e}")

    @classmethod
    def tearDownClass(cls):
        """Nettoyage de Selenium."""
        if cls.driver:
            cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        """Configuration des données de test."""
        if not self.driver:
            self.skipTest("Selenium WebDriver non disponible")

        # Vérifier que le serveur Django est accessible
        try:
            import requests

            response = requests.get("http://127.0.0.1:8000/", timeout=5)
            if response.status_code != 200:
                self.skipTest("Serveur Django non accessible")
        except Exception:
            self.skipTest("Serveur Django non accessible")

    def test_registration_with_selenium(self):
        """Test d'inscription avec Selenium."""
        # 1. Naviguer vers la page d'inscription
        self.driver.get(f"http://127.0.0.1:8000{reverse('users:signup')}")

        # 2. Attendre que la page se charge
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )

        # 3. Remplir le formulaire
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("selenium@example.com")

        first_name_field = self.driver.find_element(By.NAME, "first_name")
        first_name_field.send_keys("Selenium")

        last_name_field = self.driver.find_element(By.NAME, "last_name")
        last_name_field.send_keys("Test")

        password1_field = self.driver.find_element(By.NAME, "password1")
        password1_field.send_keys("MotDePasse123!")

        password2_field = self.driver.find_element(By.NAME, "password2")
        password2_field.send_keys("MotDePasse123!")

        # 4. Soumettre le formulaire
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )
        submit_button.click()

        # 5. Attendre la redirection
        WebDriverWait(self.driver, 10).until(EC.url_contains(reverse("users:home")))

        # 6. Vérifier que l'utilisateur a été créé
        self.assertTrue(User.objects.filter(email="selenium@example.com").exists())
        user = User.objects.get(email="selenium@example.com")
        self.assertEqual(user.username, "test.selenium")

    def test_registration_error_with_selenium(self):
        """Test d'erreur d'inscription avec Selenium."""
        # 1. Naviguer vers la page d'inscription
        self.driver.get(f"http://127.0.0.1:8000{reverse('users:signup')}")

        # 2. Remplir le formulaire avec des données invalides
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("error@example.com")

        first_name_field = self.driver.find_element(By.NAME, "first_name")
        first_name_field.send_keys("Error")

        last_name_field = self.driver.find_element(By.NAME, "last_name")
        last_name_field.send_keys("Test")

        password1_field = self.driver.find_element(By.NAME, "password1")
        password1_field.send_keys("MotDePasse123!")

        password2_field = self.driver.find_element(By.NAME, "password2")
        password2_field.send_keys("DifferentPassword456!")

        # 3. Soumettre le formulaire
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )
        submit_button.click()

        # 4. Vérifier que la page d'erreur s'affiche
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".form-error"))
        )

        # 5. Vérifier le message d'erreur
        error_message = self.driver.find_element(By.CSS_SELECTOR, ".form-error")
        self.assertIn("Les deux mots de passe ne correspondent pas", error_message.text)

        # 6. Vérifier qu'aucun utilisateur n'a été créé
        self.assertFalse(User.objects.filter(email="error@example.com").exists())
