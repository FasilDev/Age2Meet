#!/usr/bin/env python3
"""
Script pour créer des messages de test avec des messages non lus
pour tester les pastilles rouges dans la messagerie
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

def create_test_messages():
    """Créer des messages de test avec des messages non lus"""
    
    print("🔄 Création de messages de test avec des messages non lus...")
    
    try:
        # Récupérer ou créer des utilisateurs de test
        users = []
        
        # Utilisateur principal (qui va recevoir les messages non lus)
        user1, created = User.objects.get_or_create(
            username='marie.dubois',
            defaults={
                'first_name': 'Marie',
                'last_name': 'Dubois',
                'email': 'marie.dubois@example.com'
            }
        )
        users.append(user1)
        if created:
            user1.set_password('password123')
            user1.save()
            print(f"✅ Utilisateur créé: {user1.username}")
        
        # Utilisateur qui va envoyer des messages
        user2, created = User.objects.get_or_create(
            username='jean.moreau',
            defaults={
                'first_name': 'Jean',
                'last_name': 'Moreau',
                'email': 'jean.moreau@example.com'
            }
        )
        users.append(user2)
        if created:
            user2.set_password('password123')
            user2.save()
            print(f"✅ Utilisateur créé: {user2.username}")
        
        # Utilisateur qui va envoyer des messages
        user3, created = User.objects.get_or_create(
            username='pierre.bernard',
            defaults={
                'first_name': 'Pierre',
                'last_name': 'Bernard',
                'email': 'pierre.bernard@example.com'
            }
        )
        users.append(user3)
        if created:
            user3.set_password('password123')
            user3.save()
            print(f"✅ Utilisateur créé: {user3.username}")
        
        # Créer des contacts entre les utilisateurs
        contacts_to_create = [
            (user1, user2),
            (user2, user1),
            (user1, user3),
            (user3, user1),
        ]
        
        for user_from, user_to in contacts_to_create:
            contact, created = Contact.objects.get_or_create(
                user=user_from,
                contact_user=user_to,
                defaults={'status': 'accepted'}
            )
            if created:
                print(f"✅ Contact créé: {user_from.username} -> {user_to.username}")
        
        # Créer des messages avec certains non lus
        messages_to_create = [
            # Messages de Jean vers Marie (non lus)
            {
                'sender': user2,
                'receiver': user1,
                'content': 'Salut Marie ! Comment ça va ?',
                'is_read': False,
                'created_at': timezone.now() - timedelta(hours=2)
            },
            {
                'sender': user2,
                'receiver': user1,
                'content': 'Tu es libre ce week-end pour une sortie ?',
                'is_read': False,
                'created_at': timezone.now() - timedelta(hours=1)
            },
            {
                'sender': user2,
                'receiver': user1,
                'content': 'J\'ai trouvé un super restaurant !',
                'is_read': False,
                'created_at': timezone.now() - timedelta(minutes=30)
            },
            
            # Messages de Pierre vers Marie (non lus)
            {
                'sender': user3,
                'receiver': user1,
                'content': 'Coucou Marie ! On se voit toujours demain ?',
                'is_read': False,
                'created_at': timezone.now() - timedelta(hours=3)
            },
            {
                'sender': user3,
                'receiver': user1,
                'content': 'N\'oublie pas d\'apporter ton appareil photo !',
                'is_read': False,
                'created_at': timezone.now() - timedelta(minutes=15)
            },
            
            # Messages de Marie (lus, pour avoir des conversations)
            {
                'sender': user1,
                'receiver': user2,
                'content': 'Salut Jean ! Ça va bien merci.',
                'is_read': True,
                'created_at': timezone.now() - timedelta(hours=1, minutes=30)
            },
            {
                'sender': user1,
                'receiver': user3,
                'content': 'Oui Pierre, j\'ai hâte !',
                'is_read': True,
                'created_at': timezone.now() - timedelta(hours=2, minutes=45)
            },
        ]
        
        # Supprimer les anciens messages de test
        Message.objects.filter(
            content__in=[msg['content'] for msg in messages_to_create]
        ).delete()
        
        # Créer les nouveaux messages
        for msg_data in messages_to_create:
            message = Message.objects.create(**msg_data)
            status = "NON LU" if not msg_data['is_read'] else "LU"
            print(f"✅ Message créé: {msg_data['sender'].username} -> {msg_data['receiver'].username} | {status}")
        
        print("\n🎉 Messages de test créés avec succès!")
        print(f"📧 {len([m for m in messages_to_create if not m['is_read']])} messages non lus créés pour Marie")
        print(f"📝 {len(messages_to_create)} messages au total")
        
        # Afficher le résumé
        print("\n📊 Résumé des messages non lus par contact:")
        for user in [user2, user3]:
            unread_count = len([m for m in messages_to_create 
                              if m['sender'] == user and m['receiver'] == user1 and not m['is_read']])
            print(f"   {user.first_name} {user.last_name}: {unread_count} messages non lus")
        
        print("\n💡 Connectez-vous avec marie.dubois / password123 pour voir les pastilles rouges !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des messages: {e}")
        return False
    
    return True

if __name__ == '__main__':
    create_test_messages() 