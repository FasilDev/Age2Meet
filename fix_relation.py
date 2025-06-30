#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.models import Contact, User

try:
    # Récupérer les utilisateurs
    marie = User.objects.get(username='marie.dubois')
    jean = User.objects.get(username='JeanPormanove')
    
    # Trouver la relation existante
    relation = Contact.objects.get(user=marie, contact=jean)
    
    print(f'✅ Relation trouvée: {relation.user.username} -> {relation.contact.username}')
    print(f'📊 Statut avant: {relation.status}')
    
    # Changer le statut
    relation.status = 'pending'
    relation.save()
    
    print(f'📊 Statut après: {relation.status}')
    print('🎉 Relation mise à jour avec succès!')
    
    # Vérifier toutes les relations pour debug
    print('\n=== TOUTES LES RELATIONS ===')
    for contact in Contact.objects.all():
        print(f'{contact.id}: {contact.user.username} -> {contact.contact.username} ({contact.status})')
        
except Exception as e:
    print(f'❌ Erreur: {e}')
    sys.exit(1) 