JO Tickets – Projet Bloc 3 Python

Projet Django de billetterie pour les Jeux Olympiques (examen Bloc 3).  

Fonctionnalités principales :  
- Authentification sécurisée (utilisateurs, employés, administrateurs)  
- Gestion des offres et du panier  
- Passage de commande et génération de billets avec QR codes  
- Contrôle de billets par scan (réservé aux employés)  
- Interface d’administration  

---

## Installation et lancement en local

Cloner le dépôt et installer les dépendances :  

```bash
git clone https://github.com/akam731/jo-tickets.git
cd jo-tickets

python -m venv .venv

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Accéder ensuite à l’application :
http://127.0.0.1:8000
```

---

## Résumé des tests existants

### Unitaires (30)
- Modèle **User** : création, unicité email, génération `key1`  
- **Signaux** : génération automatique des clés  
- **Formulaires** : validation inscription/connexion  
- **Vues** : flux complets d’authentification  
- **Mots de passe** : règles de sécurité  

### Fonctionnels (8)
- Flux utilisateur complet (inscription + erreurs)  
- Validation des champs requis et doublons  
- Redirections après actions  

### Selenium (2)
- Inscription via navigateur réel  
- Gestion d’erreurs côté client  

## Modèle Conceptuel de Données (MCD)

👉 [Voir le MCD (PNG)](docs/MCD.png)  

Le MCD représente les entités principales (**Utilisateur**, **Offre**, **Panier**, **Commande**, **Billet**, **Scan**) et leurs associations.  

---

## Documentation

👉 [Documentation technique](docs/documentation.md)  
  *(architecture, sécurité, évolutions futures)*  

👉 [Guide utilisateur](docs/manuel.md)  
  *(parcours utilisateur complet, rôles admin/employé)*