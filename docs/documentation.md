# Documentation Technique - JO Tickets

## Architecture

### Vue d'ensemble des modules Django

```
┌─────────────────────────────────────────────────────────────────┐
│                        JO TICKETS APP                          │
├─────────────────────────────────────────────────────────────────┤
│  apps/users/          │  Authentification & gestion utilisateurs │
│  apps/catalog/        │  Gestion des offres de billets          │
│  apps/cart/           │  Panier d'achat                         │
│  apps/orders/         │  Commandes et paiements                 │
│  apps/tickets/        │  Génération et validation des billets   │
│  apps/control/        │  Interface de scan pour employés        │
│  apps/adminpanel/     │  Administration système                 │
└─────────────────────────────────────────────────────────────────┘
```

## Sécurité

### Authentification & Autorisation

- **Django Auth** : Système d'authentification intégré avec modèle User personnalisé
- **Politique MDP** : Minimum 8 caractères, validation Django par défaut
- **RBAC** : 3 rôles définis
  - `UTILISATEUR` : Achat de billets, consultation
  - `EMPLOYÉ` : Scan des billets (`is_employee=True`)
  - `ADMIN` : Administration complète (`is_adminpanel=True`)

### Protection CSRF & CORS

- **CSRF** : Token automatique sur tous les formulaires
- **CORS** : Configuration restrictive pour les API
- **CSP** : Headers de sécurité pour prévenir XSS

### Protection XSS & SQLi

- **XSS** : Échappement automatique des templates Django
- **SQLi** : ORM Django exclusivement (pas de requêtes SQL brutes)
- **Validation** : Formulaires Django avec validation côté serveur

### Génération des clés sécurisées

```python
# Clé utilisateur (key1) - générée à la création
key1 = secrets.token_urlsafe(32)

# Clé achat (key2) - générée à chaque commande
key2 = secrets.token_urlsafe(32)

# Clé finale = concaténation sécurisée
final_key = key1 + key2

# QR Code contient uniquement la final_key
# Aucune donnée personnelle dans le QR
```

### Anti-rejeu & Audit

- **Statut billet** : `valid` → `used` (irréversible)


## Évolutions futures

### Priorité Haute
1. **Transferts de billets** : Changement de propriétaire
2. **Multi-événements** : Gestion de plusieurs journées
3. **Export CSV** : Rapports de ventes

### Priorité Moyenne
5. **Tableau de bord** : Statistiques temps réel
7. **Internationalisation** : Support multilingue
8. **Accessibilité** : Conformité WCAG 2.1