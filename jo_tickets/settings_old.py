"""
Django settings for jo_tickets project.

Projet étudiant - BTS SIO
Date : Septembre 2024
"""

import os

# Determine which settings to use
if os.getenv("DJANGO_SETTINGS_MODULE") == "jo_tickets.settings.production":
    from jo_tickets.settings.production import *
else:
    from jo_tickets.settings.base import *
