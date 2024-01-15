# JO Tickets – Projet Bloc 3 Python

Projet Django de billetterie pour les Jeux Olympiques (examen Bloc 3).  

Fonctionnalités principales :  
- Authentification sécurisée (utilisateurs, employés, administrateurs)  
- Gestion des offres et du panier  
- Passage de commande et génération de billets avec QR codes  
- Contrôle de billets par scan (réservé aux employés)  
- Interface d'administration  

---

## Installation et lancement en local

### Prérequis
- Python 3.8+
- Git

### Installation

1. **Cloner le dépôt et installer les dépendances :**

```bash
git clone https://github.com/votre-username/jo-tickets.git
cd jo-tickets

python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

2. **Lancer l'application :**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Accéder ensuite à l'application :
http://127.0.0.1:8000

---

## Résumé des tests existants

### Unitaires (30)
- Modèle **User** : création, unicité email, génération `key1`  
- **Signaux** : génération automatique des clés  
- **Formulaires** : validation inscription/connexion  
- **Vues** : flux complets d'authentification  
- **Mots de passe** : règles de sécurité  

### Fonctionnels (8)
- Flux utilisateur complet (inscription + erreurs)  
- Validation des champs requis et doublons  
- Redirections après actions  

### Selenium (2)
- Inscription via navigateur réel  
- Gestion d'erreurs côté client  

## Modèle Conceptuel de Données (MCD)

Le MCD représente les entités principales (**Utilisateur**, **Offre**, **Panier**, **Commande**, **Billet**, **Scan**) et leurs associations.  

---

## Commandes utiles

### Tests
```bash
# Lancer tous les tests
python run_tests.py

# Tests unitaires uniquement
python -m pytest tests/unit/

# Tests fonctionnels
python -m pytest tests/functional/

# Tests Selenium
python run_selenium_tests.py
```

### Gestion des données
```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Charger des offres de test
python manage.py seed_offers

# Créer des billets de test
python manage.py create_tickets
```

### Développement
```bash
# Vérifier la configuration
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic

# Créer une nouvelle migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```