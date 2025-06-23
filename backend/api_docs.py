from django.http import HttpResponse
from django.views import View

class APIDocsView(View):
    """Vue temporaire pour la documentation API"""
    
    def get(self, request):
        html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Age2Meet API - Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; border-left: 4px solid #3498db; padding-left: 15px; margin-top: 30px; }
        h3 { color: #2980b9; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #28a745; }
        .method { font-weight: bold; color: white; padding: 4px 8px; border-radius: 3px; margin-right: 10px; }
        .get { background: #007bff; }
        .post { background: #28a745; }
        .put { background: #ffc107; color: black; }
        .delete { background: #dc3545; }
        code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .auth-note { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .nav { background: #3498db; color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .nav a { color: white; text-decoration: none; margin-right: 15px; }
        .nav a:hover { text-decoration: underline; }
        .example { background: #e8f5e8; padding: 10px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>🎯 Age2Meet API - Documentation</h1>
    
    <div class="nav">
        <strong>Navigation rapide:</strong>
        <a href="#auth">Authentification</a>
        <a href="#profile">Profil</a>
        <a href="#messages">Messages</a>
        <a href="#contacts">Contacts</a>
        <a href="#events">Événements</a>
        <a href="#home">Accueil</a>
    </div>
    
    <div class="auth-note">
        <strong>🔐 Authentification:</strong> Sauf mention contraire, tous les endpoints nécessitent un token d'authentification dans l'en-tête: 
        <code>Authorization: Token your_token_here</code>
    </div>
    
    <h2 id="auth">🔐 Authentification</h2>
    
    <div class="endpoint">
        <h3><span class="method post">POST</span> /api/auth/register/</h3>
        <p><strong>Description:</strong> Inscription d'un nouvel utilisateur</p>
        <p><strong>Authentification:</strong> ❌ Non requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "username": "marie_dupont",
  "email": "marie.dupont@example.com", 
  "password": "motdepasse123",
  "first_name": "Marie",
  "last_name": "Dupont",
  "date_of_birth": "1960-05-15",
  "phone": "0123456789"
}</pre>
        </div>
    </div>
    
    <div class="endpoint">
        <h3><span class="method post">POST</span> /api/auth/login/</h3>
        <p><strong>Description:</strong> Connexion utilisateur</p>
        <p><strong>Authentification:</strong> ❌ Non requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "email": "marie.dupont@example.com",
  "password": "motdepasse123"
}</pre>
        </div>
    </div>
    
    <div class="endpoint">
        <h3><span class="method post">POST</span> /api/auth/logout/</h3>
        <p><strong>Description:</strong> Déconnexion utilisateur</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
    </div>
    
    <h2 id="profile">👤 Profil Utilisateur</h2>
    
    <div class="endpoint">
        <h3><span class="method get">GET</span> /api/profile/</h3>
        <p><strong>Description:</strong> Récupérer les informations du profil</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method put">PUT</span> /api/profile/</h3>
        <p><strong>Description:</strong> Modifier les informations du profil</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "first_name": "Marie",
  "last_name": "Dupont",
  "bio": "Passionnée de jardinage et de lecture",
  "location": "Paris, France",
  "interests": "Jardinage, Lecture, Cuisine",
  "status": "online",
  "phone": "0123456789"
}</pre>
        </div>
    </div>
    
    <h2 id="messages">💬 Messagerie</h2>
    
    <div class="endpoint">
        <h3><span class="method get">GET</span> /api/messages/</h3>
        <p><strong>Description:</strong> Récupérer les messages</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <p><strong>Paramètres optionnels:</strong></p>
        <ul>
            <li><code>user_id</code> - ID de l'utilisateur pour filtrer une conversation</li>
        </ul>
    </div>
    
    <div class="endpoint">
        <h3><span class="method post">POST</span> /api/messages/</h3>
        <p><strong>Description:</strong> Envoyer un message</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "receiver_id": 2,
  "content": "Bonjour ! Comment allez-vous ?"
}</pre>
        </div>
    </div>
    
    <h2 id="contacts">👥 Contacts</h2>
    
    <div class="endpoint">
        <h3><span class="method get">GET</span> /api/contacts/</h3>
        <p><strong>Description:</strong> Récupérer la liste des contacts et demandes</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method post">POST</span> /api/contacts/</h3>
        <p><strong>Description:</strong> Envoyer une demande d'ami</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "contact_id": 3
}</pre>
        </div>
    </div>
    
    <div class="endpoint">
        <h3><span class="method put">PUT</span> /api/contacts/{id}/action/</h3>
        <p><strong>Description:</strong> Accepter/Refuser une demande d'ami</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "action": "accept"  // ou "decline"
}</pre>
        </div>
    </div>
    
    <h2 id="events">📅 Événements</h2>
    
    <div class="endpoint">
        <h3><span class="method get">GET</span> /api/events/</h3>
        <p><strong>Description:</strong> Récupérer les événements</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method post">POST</span> /api/events/</h3>
        <p><strong>Description:</strong> Créer un nouvel événement</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "title": "Atelier jardinage",
  "description": "Venez apprendre les bases du jardinage",
  "event_type": "activity",
  "location": "Jardin communautaire",
  "start_date": "2024-12-25T10:00:00",
  "end_date": "2024-12-25T12:00:00",
  "is_public": true
}</pre>
        </div>
    </div>
    
    <h2 id="home">🏠 Accueil</h2>
    
    <div class="endpoint">
        <h3><span class="method get">GET</span> /api/home/</h3>
        <p><strong>Description:</strong> Récupérer les données de la page d'accueil</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <p><strong>Retourne:</strong> Contacts suggérés, vidéos tutoriels, avis utilisateurs</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method post">POST</span> /api/reviews/</h3>
        <p><strong>Description:</strong> Laisser un avis sur le site</p>
        <p><strong>Authentification:</strong> ✅ Requis</p>
        <div class="example">
            <strong>Exemple de requête:</strong>
            <pre>{
  "rating": 5,
  "comment": "Excellent site, très facile à utiliser !"
}</pre>
        </div>
    </div>
    
    <hr style="margin: 40px 0;">
    
    <h2>📋 Notes Importantes</h2>
    
    <ul>
        <li><strong>Base URL:</strong> <code>http://localhost:8000/api/</code></li>
        <li><strong>Format:</strong> Toutes les requêtes et réponses sont en JSON</li>
        <li><strong>Token:</strong> Utilisez le token reçu lors de la connexion pour toutes les requêtes authentifiées</li>
        <li><strong>Statuts:</strong> Les statuts disponibles sont: 'online', 'away', 'busy', 'offline'</li>
        <li><strong>Dates:</strong> Format ISO 8601 (ex: "2024-12-25T10:00:00")</li>
    </ul>
    
    <div class="auth-note">
        <strong>🚀 Test rapide:</strong> Utilisez le script <code>python test_api.py</code> pour tester automatiquement tous les endpoints !
    </div>
    
    <div style="text-align: center; margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 5px;">
        <strong>Age2Meet API v1.0</strong> - Documentation temporaire<br>
        <small>Swagger sera disponible prochainement</small>
    </div>
    
</body>
</html>
        """
        return HttpResponse(html_content, content_type='text/html') 