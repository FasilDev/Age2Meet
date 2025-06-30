#!/usr/bin/env python3
"""
Script pour peupler la base de données Age2Meet avec des données de test
Usage: python populate_test_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.models import (
    User, UserProfile, Contact, Message, Event, Review, TutorialVideo,
    Activity, ActivityRegistration, Notification, UserStatistics
)

def create_users():
    """Créer des utilisateurs de test"""
    print("Création des utilisateurs...")
    
    users_data = [
        {
            'username': 'marie_martin',
            'email': 'marie.martin@example.com',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'date_of_birth': '1955-03-15',
            'phone': '0123456789',
            'password': 'testpass123'
        },
        {
            'username': 'jean_dupont',
            'email': 'jean.dupont@example.com',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'date_of_birth': '1952-07-22',
            'phone': '0987654321',
            'password': 'testpass123'
        },
        {
            'username': 'claire_bernard',
            'email': 'claire.bernard@example.com',
            'first_name': 'Claire',
            'last_name': 'Bernard',
            'date_of_birth': '1958-11-08',
            'phone': '0147258369',
            'password': 'testpass123'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'username': user_data['username'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'date_of_birth': user_data['date_of_birth'],
                'phone': user_data['phone'],
                'password': make_password(user_data['password'])
            }
        )
        if created:
            print(f"✅ Utilisateur créé: {user.first_name} {user.last_name}")
        created_users.append(user)
    
    return created_users

def create_profiles(users):
    """Créer les profils utilisateur"""
    print("\nCréation des profils...")
    
    profiles_data = [
        {
            'bio': 'Passionnée de cuisine et de jardinage. J\'adore partager mes recettes avec de nouveaux amis !',
            'location': 'Paris 15ème',
            'interests': 'Cuisine, Jardinage, Lecture, Balades en nature',
            'status': 'online'
        },
        {
            'bio': 'Retraité actif, amateur de randonnée et de photographie. Toujours prêt pour une nouvelle aventure !',
            'location': 'Lyon 6ème',
            'interests': 'Randonnée, Photographie, Histoire, Voyages',
            'status': 'online'
        },
        {
            'bio': 'Ancienne professeure d\'art, j\'anime des ateliers créatifs et cherche des compagnons de musée.',
            'location': 'Marseille 8ème',
            'interests': 'Art, Peinture, Musées, Théâtre, Danse',
            'status': 'away'
        },
        {
            'bio': 'Passionné de jeux de société et de sport doux. J\'organise des soirées jeux chez moi.',
            'location': 'Toulouse Centre',
            'interests': 'Jeux de société, Sport, Cinéma, Lecture',
            'status': 'online'
        },
        {
            'bio': 'Amatrice de café et de discussions philosophiques. Toujours partante pour un café-débat !',
            'location': 'Nice Vieux Port',
            'interests': 'Philosophie, Littérature, Café, Débats',
            'status': 'offline'
        }
    ]
    
    for i, user in enumerate(users):
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults=profiles_data[i]
        )
        if created:
            print(f"✅ Profil créé pour: {user.first_name}")

def create_contacts(users):
    """Créer des relations d'amitié"""
    print("\nCréation des contacts...")
    
    contacts_data = [
        (0, 1, 'accepted'),  # Marie <-> Jean
        (0, 2, 'accepted'),  # Marie <-> Claire
        (1, 3, 'accepted'),  # Jean <-> Robert
        (2, 4, 'pending'),   # Claire -> Sylvie (en attente)
        (3, 4, 'accepted'),  # Robert <-> Sylvie
        (1, 2, 'pending'),   # Jean -> Claire (en attente)
    ]
    
    for user1_idx, user2_idx, status in contacts_data:
        contact, created = Contact.objects.get_or_create(
            user=users[user1_idx],
            contact=users[user2_idx],
            defaults={'status': status}
        )
        if created:
            print(f"✅ Contact créé: {users[user1_idx].first_name} -> {users[user2_idx].first_name} ({status})")

def create_messages(users):
    """Créer des messages de test"""
    print("\nCréation des messages...")
    
    messages_data = [
        (0, 1, "Bonjour Jean ! Comment allez-vous aujourd'hui ?"),
        (1, 0, "Bonjour Marie ! Je vais très bien, merci. Et vous ?"),
        (0, 1, "Ça va bien ! Avez-vous vu l'activité cuisine de demain ?"),
        (1, 0, "Oui, j'ai hâte d'y participer ! Vous y serez aussi ?"),
        (0, 2, "Claire, j'ai adoré votre atelier peinture la semaine dernière !"),
        (2, 0, "Merci Marie, c'était un plaisir de vous y voir !"),
        (3, 4, "Sylvie, êtes-vous libre pour un café cet après-midi ?"),
    ]
    
    for sender_idx, receiver_idx, content in messages_data:
        message, created = Message.objects.get_or_create(
            sender=users[sender_idx],
            receiver=users[receiver_idx],
            content=content,
            defaults={'is_read': False}
        )
        if created:
            print(f"✅ Message créé de {users[sender_idx].first_name} à {users[receiver_idx].first_name}")

def create_activities(users):
    """Créer des activités de test"""
    print("\nCréation des activités...")
    
    base_date = timezone.now() + timedelta(days=1)
    
    activities_data = [
        {
            'title': 'Atelier Cuisine - Pâtisseries Traditionnelles',
            'description': 'Venez apprendre à réaliser de délicieuses pâtisseries traditionnelles françaises dans une ambiance conviviale.',
            'activity_type': 'cuisine',
            'location': 'Centre Communal de Paris 15ème',
            'address': '25 Rue de la Convention, 75015 Paris',
            'date': base_date,
            'end_date': base_date + timedelta(hours=3),
            'max_participants': 12,
            'price': 25.00,
            'difficulty': 'facile',
            'organizer': users[0],  # Marie
            'requirements': 'Tablier et bonne humeur !',
        },
        {
            'title': 'Balade Nature - Parc de la Tête d\'Or',
            'description': 'Découverte de la faune et flore du parc avec un guide naturaliste. Parfait pour les amateurs de nature !',
            'activity_type': 'balade',
            'location': 'Parc de la Tête d\'Or, Lyon',
            'address': 'Place Général Leclerc, 69006 Lyon',
            'date': base_date + timedelta(days=2),
            'end_date': base_date + timedelta(days=2, hours=2),
            'max_participants': 15,
            'price': 0.00,
            'difficulty': 'facile',
            'organizer': users[1],  # Jean
            'requirements': 'Chaussures de marche confortables',
        },
        {
            'title': 'Visite Guidée - Musée d\'Art Moderne',
            'description': 'Visite commentée des collections permanentes avec une ancienne professeure d\'art.',
            'activity_type': 'musee',
            'location': 'Musée d\'Art Moderne, Marseille',
            'address': '1 Avenue de Haïfa, 13008 Marseille',
            'date': base_date + timedelta(days=3),
            'end_date': base_date + timedelta(days=3, hours=2),
            'max_participants': 10,
            'price': 12.00,
            'difficulty': 'facile',
            'organizer': users[2],  # Claire
            'requirements': 'Billet d\'entrée au musée (7€)',
        },
        {
            'title': 'Tournoi de Jeux de Société',
            'description': 'Après-midi jeux de société avec différents niveaux. Découverte de nouveaux jeux et convivialité garantie !',
            'activity_type': 'jeux',
            'location': 'Café-Jeux "Le Dé à Jouer", Toulouse',
            'address': '15 Rue des Arts, 31000 Toulouse',
            'date': base_date + timedelta(days=5),
            'end_date': base_date + timedelta(days=5, hours=4),
            'max_participants': 16,
            'price': 8.00,
            'difficulty': 'moyen',
            'organizer': users[3],  # Robert
            'requirements': 'Aucun prérequis, tous niveaux acceptés',
        },
        {
            'title': 'Café Philo - "Le Bonheur à l\'âge d\'or"',
            'description': 'Discussion philosophique autour du thème du bonheur dans nos vies. Échange d\'idées et de réflexions.',
            'activity_type': 'cafe',
            'location': 'Café de la Place, Nice',
            'address': '12 Place Masséna, 06000 Nice',
            'date': base_date + timedelta(days=7),
            'end_date': base_date + timedelta(days=7, hours=2),
            'max_participants': 8,
            'price': 5.00,
            'difficulty': 'facile',
            'organizer': users[4],  # Sylvie
            'requirements': 'Curiosité intellectuelle et ouverture d\'esprit',
        }
    ]
    
    created_activities = []
    for activity_data in activities_data:
        activity, created = Activity.objects.get_or_create(
            title=activity_data['title'],
            defaults=activity_data
        )
        if created:
            print(f"✅ Activité créée: {activity.title}")
        created_activities.append(activity)
    
    return created_activities

def create_activity_registrations(users, activities):
    """Créer des inscriptions aux activités"""
    print("\nCréation des inscriptions...")
    
    registrations_data = [
        (1, 0, 'confirmed', 'Hâte de participer !'),        # Jean -> Cuisine de Marie
        (2, 0, 'confirmed', 'J\'adore la pâtisserie'),      # Claire -> Cuisine de Marie
        (3, 0, 'confirmed', ''),                            # Robert -> Cuisine de Marie
        (0, 1, 'confirmed', 'Parfait pour ma forme !'),     # Marie -> Balade de Jean
        (4, 1, 'confirmed', 'J\'aime la nature'),           # Sylvie -> Balade de Jean
        (0, 2, 'confirmed', 'Passionnée d\'art'),           # Marie -> Musée de Claire
        (1, 2, 'confirmed', 'Découverte intéressante'),     # Jean -> Musée de Claire
        (0, 3, 'pending', 'Premier tournoi pour moi'),      # Marie -> Jeux de Robert
        (2, 3, 'confirmed', 'J\'adore les jeux !'),         # Claire -> Jeux de Robert
        (1, 4, 'confirmed', 'Sujet passionnant'),           # Jean -> Café de Sylvie
        (3, 4, 'confirmed', 'Belle discussion en vue'),     # Robert -> Café de Sylvie
    ]
    
    for user_idx, activity_idx, status, notes in registrations_data:
        registration, created = ActivityRegistration.objects.get_or_create(
            user=users[user_idx],
            activity=activities[activity_idx],
            defaults={
                'status': status,
                'notes': notes
            }
        )
        if created:
            print(f"✅ Inscription créée: {users[user_idx].first_name} -> {activities[activity_idx].title}")

def create_events(users):
    """Créer des événements personnels"""
    print("\nCréation des événements...")
    
    base_date = timezone.now() + timedelta(days=1)
    
    events_data = [
        {
            'user': users[0],
            'title': 'Rendez-vous médecin',
            'description': 'Consultation annuelle',
            'event_type': 'personal',
            'location': 'Cabinet Dr. Martin',
            'start_date': base_date + timedelta(hours=10),
            'end_date': base_date + timedelta(hours=11),
        },
        {
            'user': users[1],
            'title': 'Anniversaire de ma fille',
            'description': 'Célébration en famille',
            'event_type': 'personal',
            'location': 'Chez moi',
            'start_date': base_date + timedelta(days=3, hours=14),
            'end_date': base_date + timedelta(days=3, hours=18),
        },
        {
            'user': users[2],
            'title': 'Cours de peinture',
            'description': 'Cours hebdomadaire d\'aquarelle',
            'event_type': 'personal',
            'location': 'Atelier d\'Art de Marseille',
            'start_date': base_date + timedelta(days=7, hours=15),
            'end_date': base_date + timedelta(days=7, hours=17),
        }
    ]
    
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            user=event_data['user'],
            title=event_data['title'],
            start_date=event_data['start_date'],
            defaults=event_data
        )
        if created:
            print(f"✅ Événement créé: {event.title} pour {event.user.first_name}")

def create_notifications(users):
    """Créer des notifications de test"""
    print("\nCréation des notifications...")
    
    notifications_data = [
        {
            'user': users[0],
            'title': 'Nouveau message',
            'message': 'Vous avez reçu un nouveau message de Jean Dupont',
            'notification_type': 'message',
            'related_object_id': 1,
        },
        {
            'user': users[2],
            'title': 'Nouvelle demande d\'ami',
            'message': 'Jean Dupont souhaite vous ajouter à ses contacts',
            'notification_type': 'contact_request',
            'related_object_id': 1,
        },
        {
            'user': users[0],
            'title': 'Rappel d\'activité',
            'message': 'N\'oubliez pas votre balade nature demain à 14h',
            'notification_type': 'activity_reminder',
            'related_object_id': 2,
        },
        {
            'user': users[4],
            'title': 'Bienvenue sur Age2Meet !',
            'message': 'Bienvenue dans notre communauté ! Découvrez toutes nos fonctionnalités.',
            'notification_type': 'welcome',
            'is_read': False,
        }
    ]
    
    for notif_data in notifications_data:
        notification, created = Notification.objects.get_or_create(
            user=notif_data['user'],
            title=notif_data['title'],
            defaults=notif_data
        )
        if created:
            print(f"✅ Notification créée pour: {notification.user.first_name}")

def create_reviews(users):
    """Créer des avis utilisateurs"""
    print("\nCréation des avis...")
    
    reviews_data = [
        {
            'user': users[0],
            'rating': 5,
            'comment': 'Excellente plateforme ! J\'ai rencontré des personnes formidables et participé à des activités enrichissantes.',
            'is_approved': True,
        },
        {
            'user': users[1],
            'rating': 4,
            'comment': 'Très bonne expérience. Les activités sont bien organisées et les membres sont accueillants.',
            'is_approved': True,
        },
        {
            'user': users[2],
            'rating': 5,
            'comment': 'Age2Meet m\'a permis de partager ma passion pour l\'art et de découvrir de nouveaux centres d\'intérêt.',
            'is_approved': True,
        }
    ]
    
    for review_data in reviews_data:
        review, created = Review.objects.get_or_create(
            user=review_data['user'],
            defaults=review_data
        )
        if created:
            print(f"✅ Avis créé par: {review.user.first_name}")

def create_statistics(users):
    """Créer les statistiques utilisateur"""
    print("\nCréation des statistiques...")
    
    for user in users:
        stats, created = UserStatistics.objects.get_or_create(
            user=user,
            defaults={
                'activities_participated': 2,
                'events_created': 1,
                'messages_sent': 3,
                'friends_count': 2,
                'profile_views': 15,
            }
        )
        if created:
            print(f"✅ Statistiques créées pour: {user.first_name}")

def create_tutorial_videos():
    """Créer des vidéos tutoriels"""
    print("\nCréation des vidéos tutoriels...")
    
    videos_data = [
        {
            'title': 'Comment créer votre profil Age2Meet',
            'description': 'Guide pas-à-pas pour optimiser votre profil',
            'video_url': 'https://example.com/video1',
            'order': 1,
        },
        {
            'title': 'Découvrir les activités disponibles',
            'description': 'Comment trouver et s\'inscrire aux activités',
            'video_url': 'https://example.com/video2',
            'order': 2,
        },
        {
            'title': 'Utiliser la messagerie',
            'description': 'Comment échanger avec les autres members',
            'video_url': 'https://example.com/video3',
            'order': 3,
        }
    ]
    
    for video_data in videos_data:
        video, created = TutorialVideo.objects.get_or_create(
            title=video_data['title'],
            defaults=video_data
        )
        if created:
            print(f"✅ Vidéo tutoriel créée: {video.title}")

def main():
    """Fonction principale"""
    print("🚀 Début du peuplement de la base de données Age2Meet\n")
    
    try:
        # Créer les données de test
        users = create_users()
        create_profiles(users)
        create_contacts(users)
        create_messages(users)
        activities = create_activities(users)
        create_activity_registrations(users, activities)
        create_events(users)
        create_notifications(users)
        create_reviews(users)
        create_statistics(users)
        create_tutorial_videos()
        
        print(f"\n✅ Peuplement terminé avec succès !")
        print(f"📊 Données créées:")
        print(f"   - {len(users)} utilisateurs")
        print(f"   - {Contact.objects.count()} relations de contact")
        print(f"   - {Message.objects.count()} messages")
        print(f"   - {len(activities)} activités")
        print(f"   - {ActivityRegistration.objects.count()} inscriptions")
        print(f"   - {Event.objects.count()} événements")
        print(f"   - {Notification.objects.count()} notifications")
        print(f"   - {Review.objects.count()} avis")
        print(f"   - {TutorialVideo.objects.count()} vidéos tutoriels")
        
        print(f"\n🔐 Connexions de test disponibles:")
        for user in users:
            print(f"   - Email: {user.email} | Mot de passe: testpass123")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 