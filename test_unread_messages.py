#!/usr/bin/env python3
"""
Script pour créer des messages de test avec des messages non lus
"""

import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Ajouter le répertoire du projet au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from backend.models import Message, Contact

def create_unread_messages():
    """Créer des messages non lus pour tester les pastilles rouges"""
    
    print("🔄 Création de messages non lus pour tester les pastilles...")
    
    try:
        # Récupérer les utilisateurs existants
        marie = User.objects.filter(username='marie.dubois').first()
        jean = User.objects.filter(username='jean.moreau').first()
        
        if not marie or not jean:
            print("❌ Utilisateurs marie.dubois ou jean.moreau non trouvés")
            print("Exécutez d'abord create_test_users.py")
            return False
        
        # Créer des messages non lus de Jean vers Marie
        test_messages = [
            {
                'sender': jean,
                'receiver': marie,
                'content': 'Salut Marie ! Tu as vu le temps magnifique aujourd\'hui ?',
                'is_read': False,
                'created_at': timezone.now() - timedelta(hours=2)
            },
            {
                'sender': jean,
                'receiver': marie,
                'content': 'On pourrait faire une balade dans le parc ?',
                'is_read': False,
                'created_at': timezone.now() - timedelta(hours=1)
            },
            {
                'sender': jean,
                'receiver': marie,
                'content': 'Réponds-moi quand tu peux ! 😊',
                'is_read': False,
                'created_at': timezone.now() - timedelta(minutes=30)
            }
        ]
        
        # Supprimer les anciens messages de test
        Message.objects.filter(
            sender=jean, 
            receiver=marie,
            content__in=[msg['content'] for msg in test_messages]
        ).delete()
        
        # Créer les nouveaux messages
        for msg_data in test_messages:
            Message.objects.create(**msg_data)
            print(f"✅ Message non lu créé: {msg_data['content'][:50]}...")
        
        print(f"\n🎉 {len(test_messages)} messages non lus créés avec succès!")
        print("💡 Connectez-vous en tant que marie.dubois pour voir les pastilles rouges")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    create_unread_messages() 