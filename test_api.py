#!/usr/bin/env python3
"""
Script de test pour l'API Age2Meet
Ce script teste les principales fonctionnalités de l'API
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_api():
    """Teste les fonctionnalités principales de l'API"""
    
    print("🚀 Test de l'API Age2Meet")
    print("=" * 50)
    
    # Test 1: Inscription
    print("\n1. Test d'inscription...")
    register_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "date_of_birth": "1960-01-01",
        "phone": "0123456789"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", 
                               json=register_data)
        if response.status_code == 201:
            print("✅ Inscription réussie")
            data = response.json()
            token = data.get('token')
            user_id = data.get('user_id')
        else:
            print(f"❌ Échec de l'inscription: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que le serveur Django est en cours d'exécution.")
        return False
    
    # Test 2: Connexion
    print("\n2. Test de connexion...")
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code == 200:
        print("✅ Connexion réussie")
        data = response.json()
        token = data.get('token')
    else:
        print(f"❌ Échec de la connexion: {response.text}")
        return False
    
    # Headers pour les requêtes authentifiées
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # Test 3: Récupération du profil
    print("\n3. Test de récupération du profil...")
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    if response.status_code == 200:
        print("✅ Profil récupéré avec succès")
        profile_data = response.json()
        print(f"   Utilisateur: {profile_data['user']['username']}")
    else:
        print(f"❌ Échec de récupération du profil: {response.text}")
    
    # Test 4: Modification du profil
    print("\n4. Test de modification du profil...")
    profile_update = {
        "bio": "Passionné de jardinage et de lecture",
        "location": "Paris, France",
        "interests": "Jardinage, Lecture, Cuisine",
        "status": "online"
    }
    
    response = requests.put(f"{BASE_URL}/profile/", 
                           json=profile_update, headers=headers)
    if response.status_code == 200:
        print("✅ Profil mis à jour avec succès")
    else:
        print(f"❌ Échec de mise à jour du profil: {response.text}")
    
    # Test 5: Page d'accueil
    print("\n5. Test de la page d'accueil...")
    response = requests.get(f"{BASE_URL}/home/", headers=headers)
    if response.status_code == 200:
        print("✅ Page d'accueil accessible")
        home_data = response.json()
        print(f"   Contacts suggérés: {len(home_data.get('suggested_contacts', []))}")
    else:
        print(f"❌ Échec d'accès à la page d'accueil: {response.text}")
    
    # Test 6: Événements
    print("\n6. Test de création d'événement...")
    event_data = {
        "title": "Atelier jardinage",
        "description": "Venez apprendre les bases du jardinage",
        "event_type": "activity",
        "location": "Jardin communautaire",
        "start_date": "2024-12-25T10:00:00",
        "end_date": "2024-12-25T12:00:00",
        "is_public": True
    }
    
    response = requests.post(f"{BASE_URL}/events/", 
                           json=event_data, headers=headers)
    if response.status_code == 201:
        print("✅ Événement créé avec succès")
    else:
        print(f"❌ Échec de création d'événement: {response.text}")
    
    # Test 7: Récupération des événements
    print("\n7. Test de récupération des événements...")
    response = requests.get(f"{BASE_URL}/events/", headers=headers)
    if response.status_code == 200:
        print("✅ Événements récupérés avec succès")
        events = response.json()
        print(f"   Nombre d'événements: {len(events)}")
    else:
        print(f"❌ Échec de récupération des événements: {response.text}")
    
    # Test 8: Avis
    print("\n8. Test de création d'avis...")
    review_data = {
        "rating": 5,
        "comment": "Excellent site, très facile à utiliser !"
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", 
                           json=review_data, headers=headers)
    if response.status_code == 201:
        print("✅ Avis créé avec succès")
    else:
        print(f"❌ Échec de création d'avis: {response.text}")
    
    # Test 9: Déconnexion
    print("\n9. Test de déconnexion...")
    response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
    if response.status_code == 200:
        print("✅ Déconnexion réussie")
    else:
        print(f"❌ Échec de déconnexion: {response.text}")
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés avec succès !")
    return True

if __name__ == "__main__":
    success = test_api()
    if not success:
        sys.exit(1) 