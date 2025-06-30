#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.models import User, UserProfile, Contact

def create_test_users():
    """Créer des utilisateurs de test pour la page Contact"""
    
    # Utilisateurs de test
    test_users = [
        {
            'username': 'marie.dubois',
            'email': 'marie.dubois@email.com',
            'first_name': 'Marie',
            'last_name': 'Dubois',
            'phone': '0123456789',
            'date_of_birth': '1950-05-15'
        },
        {
            'username': 'jean.moreau',
            'email': 'jean.moreau@email.com',
            'first_name': 'Jean',
            'last_name': 'Moreau',
            'phone': '0987654321',
            'date_of_birth': '1948-10-22'
        },
        {
            'username': 'claire.martin',
            'email': 'claire.martin@email.com',
            'first_name': 'Claire',
            'last_name': 'Martin',
            'phone': '0145789632',
            'date_of_birth': '1955-03-08'
        },
        {
            'username': 'pierre.bernard',
            'email': 'pierre.bernard@email.com',
            'first_name': 'Pierre',
            'last_name': 'Bernard',
            'phone': '0167895432',
            'date_of_birth': '1952-07-12'
        },
        {
            'username': 'sophie.petit',
            'email': 'sophie.petit@email.com',
            'first_name': 'Sophie',
            'last_name': 'Petit',
            'phone': '0198765432',
            'date_of_birth': '1951-11-25'
        }
    ]
    
    created_users = []
    
    for user_data in test_users:
        # Vérifier si l'utilisateur existe déjà
        if not User.objects.filter(email=user_data['email']).exists():
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='testpass123',  # Mot de passe par défaut
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                date_of_birth=user_data['date_of_birth']
            )
            
            # Créer/mettre à jour le profil
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.bio = f"Bonjour, je suis {user_data['first_name']} {user_data['last_name']} et j'utilise Age2Meet pour rencontrer de nouvelles personnes !"
            profile.location = "Paris, France"
            profile.interests = "Lecture, Jardinage, Cuisine, Balades"
            profile.status = 'online'
            profile.save()
            
            created_users.append(user)
            print(f"✅ Utilisateur créé: {user.first_name} {user.last_name} ({user.email})")
        else:
            print(f"⏭️  Utilisateur existant: {user_data['email']}")
    
    return created_users

def create_sample_contacts():
    """Créer des contacts de test"""
    
    # Obtenir l'utilisateur principal (celui qui est connecté)
    main_user = User.objects.filter(email='sahit.maklay@gmail.com').first()
    if not main_user:
        print("❌ Utilisateur principal non trouvé. Assurez-vous d'être inscrit avec sahit.maklay@gmail.com")
        return
    
    # Créer quelques contacts acceptés
    marie = User.objects.filter(email='marie.dubois@email.com').first()
    jean = User.objects.filter(email='jean.moreau@email.com').first()
    
    if marie:
        contact, created = Contact.objects.get_or_create(
            user=main_user,
            contact=marie,
            defaults={'status': 'accepted'}
        )
        if created:
            print(f"✅ Contact ajouté: {marie.first_name} {marie.last_name}")
    
    if jean:
        contact, created = Contact.objects.get_or_create(
            user=main_user,
            contact=jean,
            defaults={'status': 'accepted'}
        )
        if created:
            print(f"✅ Contact ajouté: {jean.first_name} {jean.last_name}")
    
    # Créer une demande en attente
    claire = User.objects.filter(email='claire.martin@email.com').first()
    if claire:
        contact, created = Contact.objects.get_or_create(
            user=claire,
            contact=main_user,
            defaults={'status': 'pending'}
        )
        if created:
            print(f"✅ Demande en attente de: {claire.first_name} {claire.last_name}")

if __name__ == '__main__':
    print("🚀 Création d'utilisateurs de test pour Age2Meet...")
    
    # Créer les utilisateurs
    created_users = create_test_users()
    
    # Créer les contacts de test
    create_sample_contacts()
    
    print("\n✅ Données de test créées avec succès !")
    print("📱 Vous pouvez maintenant tester la page Contact avec de vrais utilisateurs.")
    print("🔑 Mot de passe pour tous les utilisateurs de test: testpass123") 