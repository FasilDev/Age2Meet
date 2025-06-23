# Age2Meet - Site de Rencontres pour Personnes Âgées

## 📋 Description

Age2Meet est une plateforme de rencontres dédiée aux personnes âgées, offrant un environnement sécurisé et convivial pour créer des liens et organiser des activités.

## 🚀 Fonctionnalités

### Authentification
- ✅ Inscription avec validation d'email
- ✅ Connexion/Déconnexion sécurisée
- ✅ Gestion des tokens d'authentification

### Profil Utilisateur
- ✅ Profil personnalisable avec photo
- ✅ Statuts en temps réel (en ligne, absent, ne pas déranger)
- ✅ Informations personnelles modifiables
- ✅ Gestion des centres d'intérêt

### Messagerie
- ✅ Messages privés entre utilisateurs
- ✅ Historique des conversations
- ✅ Notifications de lecture

### Contacts/Amis
- ✅ Système de demandes d'amitié
- ✅ Gestion des contacts acceptés/refusés
- ✅ Liste des amis avec statuts

### Agenda
- ✅ Création d'événements personnels
- ✅ Événements publics visibles par tous
- ✅ Système de participation aux événements
- ✅ Différents types d'activités

### Page d'Accueil
- ✅ Découverte de nouveaux contacts
- ✅ Vidéos tutoriels pour l'utilisation du site
- ✅ Avis et témoignages d'utilisateurs

## 🛠️ Technologies Utilisées

- **Backend**: Django 5.0.6 + Django REST Framework
- **Base de données**: SQLite (développement)
- **Authentification**: Token-based authentication
- **Upload de fichiers**: Support des images de profil
- **CORS**: Configuration pour frontend séparé

## 📦 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd Age2Meet
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000`

## 📚 Documentation API

### 🌟 Interface Swagger Interactive

Après avoir lancé le serveur, vous pouvez accéder à la documentation interactive de l'API :

- **Swagger UI** : `http://localhost:8000/api/docs/` 
  - Interface moderne et interactive pour tester directement les endpoints
  - Formulaires automatiques pour tester les requêtes
  - Exemples de réponses et codes d'erreur

- **ReDoc** : `http://localhost:8000/api/redoc/`
  - Documentation alternative avec un design épuré
  - Vue d'ensemble claire de tous les endpoints

- **Schema OpenAPI** : `http://localhost:8000/api/schema/`
  - Schéma JSON brut de l'API pour intégration avec d'autres outils

### 🔧 Test de l'API avec Swagger

1. Allez sur `http://localhost:8000/api/docs/`
2. Cliquez sur "Authorize" en haut à droite
3. Créez d'abord un compte via `POST /api/auth/register/`
4. Connectez-vous via `POST /api/auth/login/` pour obtenir votre token
5. Utilisez le token dans "Authorization" (format: `Token your_token_here`)
6. Testez tous les endpoints protégés !

### 📋 Endpoints par Catégorie

### Base URL
```
http://localhost:8000/api/
```

### Authentification

#### Inscription
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "motdepasse123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1960-05-15",
    "phone": "0123456789"
}
```

#### Connexion
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "motdepasse123"
}
```

#### Déconnexion
```http
POST /api/auth/logout/
Authorization: Token your_token_here
```

### Profil

#### Récupérer le profil
```http
GET /api/profile/
Authorization: Token your_token_here
```

#### Modifier le profil
```http
PUT /api/profile/
Authorization: Token your_token_here
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Passionné de jardinage et de lecture",
    "location": "Paris, France",
    "interests": "Jardinage, Lecture, Cuisine",
    "status": "online"
}
```

### Messagerie

#### Récupérer les messages
```http
GET /api/messages/
Authorization: Token your_token_here

# Messages avec un utilisateur spécifique
GET /api/messages/?user_id=2
Authorization: Token your_token_here
```

#### Envoyer un message
```http
POST /api/messages/
Authorization: Token your_token_here
Content-Type: application/json

{
    "receiver_id": 2,
    "content": "Bonjour ! Comment allez-vous ?"
}
```

### Contacts

#### Récupérer les contacts
```http
GET /api/contacts/
Authorization: Token your_token_here
```

#### Envoyer une demande d'ami
```http
POST /api/contacts/
Authorization: Token your_token_here
Content-Type: application/json

{
    "contact_id": 2
}
```

#### Accepter/Refuser une demande
```http
PUT /api/contacts/1/action/
Authorization: Token your_token_here
Content-Type: application/json

{
    "action": "accept"  // ou "decline"
}
```

### Agenda

#### Récupérer les événements
```http
GET /api/events/
Authorization: Token your_token_here
```

#### Créer un événement
```http
POST /api/events/
Authorization: Token your_token_here
Content-Type: application/json

{
    "title": "Atelier jardinage",
    "description": "Venez apprendre les bases du jardinage",
    "event_type": "activity",
    "location": "Jardin communautaire",
    "start_date": "2024-06-15T10:00:00",
    "end_date": "2024-06-15T12:00:00",
    "is_public": true
}
```

### Page d'Accueil

#### Récupérer les données d'accueil
```http
GET /api/home/
Authorization: Token your_token_here
```

### Avis

#### Laisser un avis
```http
POST /api/reviews/
Authorization: Token your_token_here
Content-Type: application/json

{
    "rating": 5,
    "comment": "Excellent site, très facile à utiliser !"
}
```

## 🔒 Sécurité

- Authentification par token
- Validation des données côté serveur
- CORS configuré pour le frontend
- Passwords hashés avec Django
- Validation des permissions sur toutes les routes

## 🗄️ Modèles de Données

### User (Utilisateur personnalisé)
- username, email, first_name, last_name
- date_of_birth, phone
- created_at, updated_at

### UserProfile
- bio, location, interests
- status (online/away/busy/offline)
- profile_picture, is_verified

### Contact
- user, contact, status
- (pending/accepted/declined/blocked)

### Message
- sender, receiver, content
- is_read, created_at

### Event
- title, description, event_type
- location, start_date, end_date
- attendees, is_public

### Review
- user, rating (1-5), comment
- is_approved

### TutorialVideo
- title, description, video_url
- thumbnail, order, is_active

## 🎯 Administration

Interface d'administration Django disponible sur `/admin/`

Fonctionnalités:
- Gestion des utilisateurs et profils
- Modération des messages et avis
- Gestion des événements
- Administration des vidéos tutoriels

## 🔧 Configuration

### Variables d'environnement
Vous pouvez créer un fichier `.env` pour la configuration :

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### CORS
Configuré pour accepter les requêtes depuis :
- http://localhost:3000
- http://127.0.0.1:3000

## 📱 Structure des Réponses API

### Succès
```json
{
    "message": "Opération réussie",
    "data": { ... }
}
```

### Erreur
```json
{
    "error": "Description de l'erreur"
}
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre feature
3. Commit vos changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.

## 📞 Support

Pour toute question ou support, contactez l'équipe de développement. 