#!/usr/bin/env python3
"""
Script pour tester toutes les routes de l'API Age2Meet
"""
import requests
import json

BASE_URL = "http://127.0.0.1:3000/api"  # Changez le port ici

def test_register():
    """Test de l'inscription"""
    print("=== Test Inscription ===")
    data = {
        "username": "marie_dupont",
        "email": "marie.dupont@example.com",
        "password": "motdepasse123",
        "first_name": "Marie",
        "last_name": "Dupont",
        "date_of_birth": "1995-05-15",
        "phone": "0123456789"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('token') if response.status_code == 201 else None

def test_login():
    """Test de la connexion"""
    print("\n=== Test Connexion ===")
    data = {
        "email": "marie.dupont@example.com",
        "password": "motdepasse123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('token') if response.status_code == 200 else None

def test_profile(token):
    """Test du profil"""
    print("\n=== Test Profil ===")
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_messages(token):
    """Test des messages"""
    print("\n=== Test Messages ===")
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/messages/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_events(token):
    """Test des événements"""
    print("\n=== Test Événements ===")
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/events/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_contacts(token):
    """Test des contacts"""
    print("\n=== Test Contacts ===")
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/contacts/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_logout(token):
    """Test de la déconnexion"""
    print("\n=== Test Déconnexion ===")
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    """Fonction principale"""
    print("🚀 Test de toutes les routes API Age2Meet\n")
    
    # Test inscription
    token = test_register()
    
    if not token:
        # Si l'inscription échoue, essayez la connexion
        token = test_login()
    
    if token:
        print(f"\n🔑 Token obtenu: {token}")
        
        # Test des routes protégées
        test_profile(token)
        test_messages(token)
        test_events(token)
        test_contacts(token)
        test_logout(token)
    else:
        print("❌ Impossible d'obtenir un token")

if __name__ == "__main__":
    main() 