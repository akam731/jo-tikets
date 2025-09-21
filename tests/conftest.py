"""
Configuration globale pour les tests de l'application JO Tickets.

Ce fichier contient les fixtures et configurations partagées
entre tous les tests.
"""

import os
import django
from django.test import TestCase

# Configuration Django pour les tests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jo_tickets.settings")
django.setup()


class BaseTestCase(TestCase):
    """
    Classe de base pour tous les tests de l'application.

    Contient les configurations et utilitaires communs.
    """

    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests."""
        super().setUpClass()
        # Configuration spécifique aux tests si nécessaire
        pass

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests."""
        super().tearDownClass()
        # Nettoyage spécifique si nécessaire
        pass
