# Guide Utilisateur - JO Tickets

## Pré-requis

### Compte utilisateur
- Adresse email valide
- Mot de passe sécurisé (minimum 8 caractères)
- Nom et prénom

### Accès à l'application
- **URL locale** : http://127.0.0.1:8000/
- **Navigateur recommandé** : Chrome, Firefox

---

## Création d'un compte

### 1. Accéder au formulaire d'inscription
1. Cliquez sur **"S'inscrire"** dans le menu principal
2. Remplissez le formulaire d'inscription

### 2. Règles de mot de passe
- **Minimum 8 caractères**
- **Recommandé** : Majuscules, minuscules, chiffres et symboles
- **Exemple valide** : `MonMotDePasse123!`

### 3. Validation du compte
- Connectez-vous avec vos identifiants

---

## Parcourir les offres

### Types d'offres disponibles par défaut

#### Solo (1 personne)
- **Prix** : 25€
- **Capacité** : 1 personne
- **Idéal pour** : Visite individuelle

#### Duo (2 personnes)
- **Prix** : 45€
- **Capacité** : 2 personnes
- **Idéal pour** : Couples, amis

#### Familiale (4 personnes)
- **Prix** : 80€
- **Capacité** : 4 personnes
- **Idéal pour** : Familles

### Ajouter au panier
1. **Sélectionnez** l'offre
2. **Cliquez** sur "Ajouter au panier"

---

## Validation de la commande

### 1. Vérification du panier
- **Articles** : Vérifiez les offres sélectionnées
- **Quantités** : Contrôlez les nombres
- **Total** : Vérifiez le montant final

### 2. Procédure de paiement
1. **Cliquez** sur "Finaliser la commande"
2. **Sélectionnez** une méthode de paiement
3. **Cliquez** sur "Payer XX €"

> **Note** : Le paiement est simulé pour la démonstration. Aucun vrai paiement n'est effectué.

### 3. Confirmation
- **Message de succès** : "Paiement effectué avec succès"
- **Redirection** : Vers la page "Mes Billets"

---

## Récupération du e-billet

### 1. Accès aux billets
1. **Connectez-vous** à votre compte
2. **Cliquez** sur "Mes billets" dans le menu
3. **Sélectionnez** le billet à visualiser "Voir détails"

### 2. Informations du billet
- **QR Code** : Code à scanner à l'entrée
- **Clé finale** : Identifiant unique du billet
- **Statut** : Valide/Utilisé
- **Détails** : Offre, date d'achat ...

### 3. Actions disponibles
- **Copier la clé** : Clé disponible en dessous du QR Code
- **Presenter** : le QR code

---

## Espace Administrateur

### Accès
- **Lien** : "Administration" disponible dans le menu

### Gestion des offres (CRUD)

#### Créer une offre
1. **Cliquez** sur "Nouvelle offre"
2. **Remplissez** : Nom, capacité, prix, description
3. **Activez** l'offre si nécessaire
4. **Sauvegardez**

#### Modifier une offre
1. **Sélectionnez** l'offre à modifier
2. **Cliquez** sur "Modifier"
3. **Ajustez** les informations
4. **Sauvegardez**

#### Supprimer une offre
1. **Sélectionnez** l'offre
2. **Cliquez** sur "Supprimer"
3. **Confirmez** la suppression

### Statistiques de ventes
- **Ventes par offre** : Revenus propres à chaque offre
- **Revenus totaux** : Montant des ventes
- **Billets vendus** : Nombre total
- **Offres actives** : Nombre d'offres actives

---

## Espace Employé (Scan)

### Accès
- **Lien** : "Scanner" disponible dans le menu

### Scanner un QR code
1. **Autorisez** l'accès à la caméra
2. **Positionnez** le QR code dans le cadre
3. **Attendez** la validation automatique

### Saisie manuelle
1. **Copiez** la clé finale du billet
2. **Collez** dans le champ de saisie
3. **Cliquez** sur "Valider le billet"

### Résultats du scan

#### Billet valide
- **Statut** : Validé avec succès
- **Propriétaire** : Nom du détenteur
- **Offre** : Type d'offre
- **Date d'achat** : Date d'achat du billet

#### Billet déjà utilisé
- **Statut** : Déjà utilisé
- **Informations** : Détails du billet

#### Billet invalide
- **Statut** : Billet introuvable
- **Vérification** : Vérifiez la clé saisie