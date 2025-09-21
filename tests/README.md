# Tests de l'application JO Tickets

Ce dossier contient tous les tests de l'application organisés par type.

## Structure des tests

```
tests/
├── __init__.py                 # Configuration du package de tests
├── conftest.py                 # Configuration globale et fixtures
├── README.md                   # Ce fichier
├── unit/                       # Tests unitaires
│   ├── __init__.py
│   └── test_users.py          # Tests unitaires des utilisateurs
├── functional/                 # Tests fonctionnels
│   ├── __init__.py
│   └── test_user_registration.py  # Tests fonctionnels d'inscription
└── integration/                # Tests d'intégration
    └── __init__.py
```

## Types de tests

### Tests unitaires (`unit/`)
- **Objectif** : Tester les composants individuels de manière isolée
- **Exemples** : Modèles, vues, formulaires, utilitaires
- **Caractéristiques** : Rapides, isolés, pas de base de données réelle

### Tests fonctionnels (`functional/`)
- **Objectif** : Tester le comportement de l'application du point de vue utilisateur
- **Exemples** : Flux d'inscription, processus de commande, navigation
- **Caractéristiques** : Simulent l'interaction utilisateur réelle

### Tests d'intégration (`integration/`)
- **Objectif** : Tester l'interaction entre différents composants
- **Exemples** : API externes, services, intégrations
- **Caractéristiques** : Testent les interfaces entre composants

## Comment lancer les tests

### Avec le script personnalisé
```bash
# Tous les tests
python run_tests.py

# Tests unitaires seulement
python run_tests.py --unit

# Tests fonctionnels seulement
python run_tests.py --functional

# Tests Selenium seulement
python run_tests.py --selenium

# Avec couverture de code
python run_tests.py --coverage

# Mode verbeux
python run_tests.py --verbose
```

### Avec Django directement
```bash
# Tous les tests
python manage.py test tests

# Tests unitaires
python manage.py test tests.unit

# Tests fonctionnels
python manage.py test tests.functional

# Tests d'intégration
python manage.py test tests.integration

# Tests spécifiques
python manage.py test tests.unit.test_users
python manage.py test tests.functional.test_user_registration
```

### Avec pytest
```bash
# Tous les tests
pytest tests/

# Tests unitaires
pytest tests/unit/

# Tests fonctionnels
pytest tests/functional/

# Avec couverture
pytest --cov=. tests/
```

## Configuration

- **Django** : Utilise `jo_tickets.settings` par défaut
- **Base de données** : Base de données de test en mémoire
- **Selenium** : Chrome en mode headless (sans interface graphique)

## Ajout de nouveaux tests

1. **Tests unitaires** : Ajouter dans `tests/unit/test_[module].py`
2. **Tests fonctionnels** : Ajouter dans `tests/functional/test_[fonctionnalité].py`
3. **Tests d'intégration** : Ajouter dans `tests/integration/test_[intégration].py`

## Bonnes pratiques

- Nommer les fichiers de test avec le préfixe `test_`
- Nommer les classes de test avec le suffixe `Test`
- Nommer les méthodes de test avec le préfixe `test_`
- Utiliser des noms descriptifs pour les tests
- Grouper les tests par fonctionnalité
- Utiliser des fixtures pour les données de test communes
