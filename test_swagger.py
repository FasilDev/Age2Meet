#!/usr/bin/env python3
"""
Script de test pour vérifier que Swagger fonctionne
"""

import requests
import webbrowser
import time
import sys

BASE_URL = "http://localhost:8000"

def test_swagger():
    """Teste l'accessibilité de Swagger"""
    
    print("🔍 Test de l'accessibilité de Swagger...")
    print("=" * 50)
    
    # Test 1: Vérifier que le serveur fonctionne
    print("\n1. Vérification du serveur...")
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        print("✅ Serveur Django accessible")
    except requests.exceptions.ConnectionError:
        print("❌ Serveur Django non accessible. Assurez-vous qu'il fonctionne avec:")
        print("   python manage.py runserver")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout - le serveur met trop de temps à répondre")
        return False
    
    # Test 2: Vérifier le schéma OpenAPI
    print("\n2. Test du schéma OpenAPI...")
    try:
        response = requests.get(f"{BASE_URL}/api/schema/", timeout=10)
        if response.status_code == 200:
            print("✅ Schéma OpenAPI généré avec succès")
            schema = response.json()
            print(f"   Version OpenAPI: {schema.get('openapi', 'N/A')}")
            print(f"   Titre: {schema.get('info', {}).get('title', 'N/A')}")
            print(f"   Version API: {schema.get('info', {}).get('version', 'N/A')}")
            print(f"   Nombre d'endpoints: {len(schema.get('paths', {}))}")
        else:
            print(f"❌ Erreur génération schéma: {response.status_code}")
            print(f"   Réponse: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test du schéma: {e}")
        return False
    
    # Test 3: Vérifier Swagger UI
    print("\n3. Test de Swagger UI...")
    try:
        response = requests.get(f"{BASE_URL}/api/docs/", timeout=10)
        if response.status_code == 200:
            print("✅ Swagger UI accessible")
        else:
            print(f"❌ Swagger UI non accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de Swagger UI: {e}")
        return False
    
    # Test 4: Vérifier ReDoc
    print("\n4. Test de ReDoc...")
    try:
        response = requests.get(f"{BASE_URL}/api/redoc/", timeout=10)
        if response.status_code == 200:
            print("✅ ReDoc accessible")
        else:
            print(f"❌ ReDoc non accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de ReDoc: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Swagger configuré avec succès !")
    print("\n📋 URLs disponibles:")
    print(f"   • Swagger UI: {BASE_URL}/api/docs/")
    print(f"   • ReDoc:      {BASE_URL}/api/redoc/") 
    print(f"   • Schema:     {BASE_URL}/api/schema/")
    
    # Proposer d'ouvrir Swagger
    choice = input("\n🌐 Voulez-vous ouvrir Swagger UI dans votre navigateur ? (y/N): ")
    if choice.lower() in ['y', 'yes', 'o', 'oui']:
        print("🚀 Ouverture de Swagger UI...")
        webbrowser.open(f"{BASE_URL}/api/docs/")
    
    return True

if __name__ == "__main__":
    try:
        success = test_swagger()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(0) 