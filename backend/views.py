from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
import json
from datetime import datetime, timedelta

from .models import User, UserProfile, Contact, Message, Event, Review, TutorialVideo, Activity, ActivityRegistration, Notification, UserStatistics
from .serializers import *

# ===== VUES D'AUTHENTIFICATION =====

class RegisterView(APIView):
    """Vue pour l'inscription"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = request.data
            
            # Vérifier si l'email existe déjà
            if User.objects.filter(email=data.get('email')).exists():
                return Response({'error': 'Cet email est déjà utilisé'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                date_of_birth=data.get('date_of_birth'),
                phone=data.get('phone', '')
            )
            
            # Créer le profil utilisateur
            profile = UserProfile.objects.create(user=user)
            
            # Créer le token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Inscription réussie',
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """Vue pour la connexion"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            user = authenticate(username=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                
                # Option 1: Ne pas forcer le statut - garder le statut précédent
                # profile = user.profile
                # profile.status = 'online'  # Commenté pour garder le statut choisi
                # profile.save()
                
                # Option 2: Mettre 'online' seulement si c'était 'offline'
                profile = user.profile
                if profile.status == 'offline':
                    profile.status = 'online'
                    profile.save()
                # Si c'était 'busy' ou 'away', on garde ce statut
                
                return Response({
                    'message': 'Connexion réussie',
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email ou mot de passe incorrect'}, 
                              status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """Vue pour la déconnexion"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Option: Ne forcer 'offline' que si l'utilisateur était 'online'
            profile = request.user.profile
            if profile.status == 'online':
                profile.status = 'offline'
                profile.save()
            # Si c'était 'busy' ou 'away', on garde ce statut même déconnecté
            
            # Supprimer le token
            request.user.auth_token.delete()
            
            return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES DE PROFIL =====

class ProfileView(APIView):
    """Vue pour gérer le profil utilisateur"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les informations du profil"""
        try:
            profile = request.user.profile
            data = {
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'date_of_birth': request.user.date_of_birth,
                    'phone': request.user.phone,
                },
                'profile': {
                    'bio': profile.bio,
                    'location': profile.location,
                    'interests': profile.interests,
                    'status': profile.status,
                    'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
                    'is_verified': profile.is_verified,
                }
            }
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        def put(self, request):
            """Modifier les informations du profil"""
            try:
                user = request.user
                profile = user.profile
                data = request.data
                
                print(f"📤 Données reçues: {data}")
                print(f"📤 Fichiers reçus: {request.FILES}")
                
                # Mettre à jour les informations utilisateur
                user.first_name = data.get('first_name', user.first_name)
                user.last_name = data.get('last_name', user.last_name)
                user.phone = data.get('phone', user.phone)
                user.save()
                
                # Mettre à jour le profil
                profile.bio = data.get('bio', profile.bio)
                profile.location = data.get('location', profile.location)
                profile.interests = data.get('interests', profile.interests)
                profile.status = data.get('status', profile.status)
                
                # Gérer l'upload de photo de profil
                if 'profile_picture' in request.FILES:
                    uploaded_file = request.FILES['profile_picture']
                    print(f"📤 Fichier uploadé: {uploaded_file.name}")
                    print(f"📤 Taille: {uploaded_file.size} bytes")
                    print(f"📤 Type: {uploaded_file.content_type}")
                    
                    profile.profile_picture = uploaded_file
                    profile.save()
                    
                    print(f"📁 Fichier sauvé à: {profile.profile_picture.path}")
                    print(f"🔗 URL générée: {profile.profile_picture.url}")
                    
                    # Vérifier que le fichier existe physiquement
                    import os
                    if os.path.exists(profile.profile_picture.path):
                        print(f"✅ Fichier physique existe: {profile.profile_picture.path}")
                    else:
                        print(f"❌ Fichier physique n'existe pas: {profile.profile_picture.path}")
                
                profile.save()
                
                # Retourner les données complètes
                response_data = {
                    'message': 'Profil mis à jour avec succès',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'date_of_birth': user.date_of_birth,
                        'phone': user.phone,
                    },
                    'profile': {
                        'bio': profile.bio,
                        'location': profile.location,
                        'interests': profile.interests,
                        'status': profile.status,
                        'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
                        'is_verified': profile.is_verified,
                    }
                }
                
                print(f"📦 Réponse envoyée: {response_data}")
                
                return Response(response_data, status=status.HTTP_200_OK)
                
            except Exception as e:
                print(f"❌ Erreur: {e}")
                import traceback
                traceback.print_exc()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES DE MESSAGERIE =====

class MessageView(APIView):
    """Vue pour la messagerie"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les messages de l'utilisateur"""
        try:
            user_id = request.GET.get('user_id')
            
            if user_id:
                # Messages avec un utilisateur spécifique
                messages = Message.objects.filter(
                    Q(sender=request.user, receiver_id=user_id) |
                    Q(sender_id=user_id, receiver=request.user)
                ).order_by('created_at')
                
                # Marquer les messages reçus comme lus
                Message.objects.filter(
                    sender_id=user_id, 
                    receiver=request.user, 
                    is_read=False
                ).update(is_read=True)
                
            else:
                # Tous les messages reçus
                messages = Message.objects.filter(receiver=request.user)
            
            data = []
            for message in messages:
                data.append({
                    'id': message.id,
                    'sender': {
                        'id': message.sender.id,
                        'username': message.sender.username,
                        'first_name': message.sender.first_name,
                        'last_name': message.sender.last_name,
                    },
                    'receiver': {
                        'id': message.receiver.id,
                        'username': message.receiver.username,
                        'first_name': message.receiver.first_name,
                        'last_name': message.receiver.last_name,
                    },
                    'content': message.content,
                    'is_read': message.is_read,
                    'created_at': message.created_at.isoformat(),
                })
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """Envoyer un message"""
        try:
            receiver_id = request.data.get('receiver_id')
            content = request.data.get('content')
            
            if not receiver_id or not content:
                return Response({'error': 'Destinataire et contenu requis'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            receiver = get_object_or_404(User, id=receiver_id)
            
            # Vérifier si les utilisateurs sont amis
            contact = Contact.objects.filter(
                Q(user=request.user, contact=receiver, status='accepted') |
                Q(user=receiver, contact=request.user, status='accepted')
            ).exists()
            
            if not contact:
                return Response({'error': 'Vous devez être amis pour envoyer un message'}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )
            
            return Response({
                'message': 'Message envoyé avec succès',
                'message_id': message.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES DE CONTACTS =====

class ContactView(APIView):
    """Vue pour gérer les contacts/amis"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer la liste des contacts"""
        try:
            # Contacts acceptés
            accepted_contacts = Contact.objects.filter(
                Q(user=request.user, status='accepted') |
                Q(contact=request.user, status='accepted')
            )
            
            # Demandes REÇUES (en attente)
            pending_requests = Contact.objects.filter(
                contact=request.user,
                status='pending'
            )
            
            # Demandes ENVOYÉES (en attente)
            sent_requests = Contact.objects.filter(
                user=request.user,
                status='pending'
            )
            
            contacts_data = []
            for contact in accepted_contacts:
                friend = contact.contact if contact.user == request.user else contact.user
                contacts_data.append({
                    'id': friend.id,
                    'username': friend.username,
                    'first_name': friend.first_name,
                    'last_name': friend.last_name,
                    'email': friend.email,
                    'bio': friend.profile.bio or '',
                    'location': friend.profile.location or '',
                    'interests': friend.profile.interests or '',
                    'status': friend.profile.status,
                    'profile_picture': friend.profile.profile_picture.url if friend.profile.profile_picture else None,
                    'contact_relation_id': contact.id,
                })
            
            requests_data = []
            for request_obj in pending_requests:
                requests_data.append({
                    'id': request_obj.id,
                    'user': {
                        'id': request_obj.user.id,
                        'username': request_obj.user.username,
                        'first_name': request_obj.user.first_name,
                        'last_name': request_obj.user.last_name,
                    },
                    'created_at': request_obj.created_at.isoformat(),
                })
            
            sent_requests_data = []
            for request_obj in sent_requests:
                sent_requests_data.append({
                    'id': request_obj.id,
                    'contact': {
                        'id': request_obj.contact.id,
                        'username': request_obj.contact.username,
                        'first_name': request_obj.contact.first_name,
                        'last_name': request_obj.contact.last_name,
                        'email': request_obj.contact.email,
                        'bio': request_obj.contact.profile.bio or '',
                        'location': request_obj.contact.profile.location or '',
                        'interests': request_obj.contact.profile.interests or '',
                        'status': request_obj.contact.profile.status,
                        'profile_picture': request_obj.contact.profile.profile_picture.url if request_obj.contact.profile.profile_picture else None,
                    },
                    'created_at': request_obj.created_at.isoformat(),
                })
            
            return Response({
                'accepted_contacts': contacts_data,
                'pending_requests': requests_data,
                'sent_requests': sent_requests_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """Envoyer une demande d'ami"""
        try:
            contact_id = request.data.get('contact_id')
            
            if not contact_id:
                return Response({'error': 'ID du contact requis'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            contact_user = get_object_or_404(User, id=contact_id)
            
            if contact_user == request.user:
                return Response({'error': 'Vous ne pouvez pas vous ajouter vous-même'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier si une relation active existe déjà (accepted ou pending)
            existing_active = Contact.objects.filter(
                Q(user=request.user, contact=contact_user) |
                Q(user=contact_user, contact=request.user)
            ).filter(status__in=['accepted', 'pending']).first()
            
            if existing_active:
                return Response({'error': 'Relation déjà existante'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Chercher une relation declined qui pourrait être réactivée
            existing_declined = Contact.objects.filter(
                user=request.user, 
                contact=contact_user,
                status='declined'
            ).first()
            
            if existing_declined:
                # Réactiver la relation declined
                existing_declined.status = 'pending'
                existing_declined.created_at = timezone.now()  # Mettre à jour la date
                existing_declined.save()
                
                return Response({
                    'message': 'Demande d\'ami renvoyée',
                    'contact_id': existing_declined.id
                }, status=status.HTTP_200_OK)
            else:
                # Créer une nouvelle relation
                contact = Contact.objects.create(
                    user=request.user,
                    contact=contact_user,
                    status='pending'
                )
                
                return Response({
                    'message': 'Demande d\'ami envoyée',
                    'contact_id': contact.id
                }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ContactActionView(APIView):
    """Vue pour accepter/refuser une demande d'ami"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, contact_id):
        """Accepter ou refuser une demande"""
        try:
            action = request.data.get('action')  # 'accept' ou 'decline'
            
            contact = get_object_or_404(Contact, id=contact_id, contact=request.user)
            
            if action == 'accept':
                contact.status = 'accepted'
                message = 'Demande d\'ami acceptée'
            elif action == 'decline':
                contact.status = 'declined'
                message = 'Demande d\'ami refusée'
            else:
                return Response({'error': 'Action non valide'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            contact.save()
            
            return Response({'message': message}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ContactDeleteView(APIView):
    """Vue pour supprimer/retirer un ami"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, contact_id):
        """Supprimer une relation d'amitié"""
        try:
            # Chercher la relation dans les deux sens
            contact = Contact.objects.filter(
                Q(id=contact_id, user=request.user) |
                Q(id=contact_id, contact=request.user)
            ).first()
            
            if not contact:
                return Response({'error': 'Contact non trouvé'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Vérifier que l'utilisateur a le droit de supprimer cette relation
            if contact.user != request.user and contact.contact != request.user:
                return Response({'error': 'Non autorisé'}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            contact.delete()
            
            return Response({'message': 'Contact supprimé avec succès'}, 
                          status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES D'AGENDA =====

class EventView(APIView):
    """Vue pour gérer les événements"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les événements de l'utilisateur"""
        try:
            # Événements de l'utilisateur + événements publics
            user_events = Event.objects.filter(user=request.user)
            public_events = Event.objects.filter(is_public=True).exclude(user=request.user)
            
            # Combiner les querysets manuellement pour éviter l'erreur SQL
            all_events = list(user_events) + list(public_events)
            
            events_data = []
            for event in all_events:
                events_data.append({
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'event_type': event.event_type,
                    'location': event.location,
                    'start_date': event.start_date.isoformat(),
                    'end_date': event.end_date.isoformat(),
                    'is_public': event.is_public,
                    'is_owner': event.user == request.user,
                    'organizer': {
                        'id': event.user.id,
                        'username': event.user.username,
                        'first_name': event.user.first_name,
                        'last_name': event.user.last_name,
                    },
                    'attendees_count': event.attendees.count(),
                    'is_attending': request.user in event.attendees.all(),
                })
            
            return Response(events_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """Créer un nouvel événement"""
        try:
            data = request.data
            
            event = Event.objects.create(
                user=request.user,
                title=data.get('title'),
                description=data.get('description', ''),
                event_type=data.get('event_type', 'personal'),
                location=data.get('location', ''),
                start_date=datetime.fromisoformat(data.get('start_date')),
                end_date=datetime.fromisoformat(data.get('end_date')),
                is_public=data.get('is_public', False)
            )
            
            return Response({
                'message': 'Événement créé avec succès',
                'event_id': event.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES D'ACCUEIL =====

class HomeView(APIView):
    """Vue pour la page d'accueil"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les données de la page d'accueil"""
        try:
            # Nouveaux contacts suggérés (utilisateurs pas encore ajoutés)
            existing_contacts = Contact.objects.filter(
                Q(user=request.user) | Q(contact=request.user)
            ).values_list('user_id', 'contact_id')
            
            excluded_ids = set()
            for user_id, contact_id in existing_contacts:
                excluded_ids.add(user_id)
                excluded_ids.add(contact_id)
            excluded_ids.add(request.user.id)
            
            suggested_contacts = User.objects.exclude(id__in=excluded_ids)[:10]
            
            # Vidéos tutoriels
            tutorial_videos = TutorialVideo.objects.filter(is_active=True)[:5]
            
            # Avis approuvés
            reviews = Review.objects.filter(is_approved=True)[:5]
            
            # Données de réponse
            data = {
                'suggested_contacts': [
                    {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'profile_picture': user.profile.profile_picture.url if user.profile.profile_picture else None,
                        'location': user.profile.location,
                        'interests': user.profile.interests,
                    }
                    for user in suggested_contacts
                ],
                'tutorial_videos': [
                    {
                        'id': video.id,
                        'title': video.title,
                        'description': video.description,
                        'video_url': video.video_url,
                        'thumbnail': video.thumbnail.url if video.thumbnail else None,
                    }
                    for video in tutorial_videos
                ],
                'reviews': [
                    {
                        'id': review.id,
                        'user': {
                            'username': review.user.username,
                            'first_name': review.user.first_name,
                            'last_name': review.user.last_name,
                        },
                        'rating': review.rating,
                        'comment': review.comment,
                        'created_at': review.created_at.isoformat(),
                    }
                    for review in reviews
                ]
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReviewView(APIView):
    """Vue pour les avis utilisateurs"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Créer un avis"""
        try:
            data = request.data
            
            # Vérifier si l'utilisateur a déjà laissé un avis
            if Review.objects.filter(user=request.user).exists():
                return Response({'error': 'Vous avez déjà laissé un avis'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            review = Review.objects.create(
                user=request.user,
                rating=data.get('rating'),
                comment=data.get('comment', '')
            )
            
            return Response({
                'message': 'Avis soumis avec succès. Il sera vérifié avant publication.',
                'review_id': review.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES ACTIVITÉS =====

class ActivityView(APIView):
    """Vue pour gérer les activités Age2meet"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les activités disponibles"""
        try:
            # Filtres optionnels
            activity_type = request.GET.get('type')
            location = request.GET.get('location')
            date_from = request.GET.get('date_from')
            date_to = request.GET.get('date_to')
            
            activities = Activity.objects.filter(is_active=True, date__gte=timezone.now())
            
            if activity_type:
                activities = activities.filter(activity_type=activity_type)
            if location:
                activities = activities.filter(location__icontains=location)
            if date_from:
                activities = activities.filter(date__gte=datetime.fromisoformat(date_from))
            if date_to:
                activities = activities.filter(date__lte=datetime.fromisoformat(date_to))
            
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """Créer une nouvelle activité (pour les organisateurs)"""
        try:
            serializer = ActivityCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                activity = serializer.save()
                return Response({
                    'message': 'Activité créée avec succès',
                    'activity_id': activity.id
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetailView(APIView):
    """Vue pour les détails d'une activité"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, activity_id):
        """Récupérer les détails d'une activité"""
        try:
            activity = get_object_or_404(Activity, id=activity_id, is_active=True)
            serializer = ActivitySerializer(activity, context={'request': request})
            
            # Ajouter la liste des participants
            participants = ActivityRegistration.objects.filter(
                activity=activity, 
                status='confirmed'
            ).select_related('user')
            
            participants_data = [{
                'id': reg.user.id,
                'username': reg.user.username,
                'first_name': reg.user.first_name,
                'last_name': reg.user.last_name,
                'registration_date': reg.registration_date.isoformat(),
            } for reg in participants]
            
            data = serializer.data
            data['participants'] = participants_data
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ActivityRegistrationView(APIView):
    """Vue pour les inscriptions aux activités"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """S'inscrire à une activité"""
        try:
            activity_id = request.data.get('activity_id')
            activity = get_object_or_404(Activity, id=activity_id, is_active=True)
            
            # Vérifier si l'activité n'est pas complète
            if activity.is_full:
                return Response({'error': 'Cette activité est complète'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier si l'utilisateur n'est pas déjà inscrit
            if ActivityRegistration.objects.filter(user=request.user, activity=activity).exists():
                return Response({'error': 'Vous êtes déjà inscrit à cette activité'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Créer l'inscription
            registration = ActivityRegistration.objects.create(
                user=request.user,
                activity=activity,
                notes=request.data.get('notes', ''),
                status='confirmed'
            )
            
            # Créer une notification pour l'organisateur
            Notification.objects.create(
                user=activity.organizer,
                title='Nouvelle inscription',
                message=f'{request.user.first_name} {request.user.last_name} s\'est inscrit à votre activité "{activity.title}"',
                notification_type='activity_reminder',
                related_object_id=activity.id
            )
            
            return Response({
                'message': 'Inscription réussie !',
                'registration_id': registration.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, registration_id):
        """Annuler une inscription"""
        try:
            registration = get_object_or_404(
                ActivityRegistration, 
                id=registration_id, 
                user=request.user
            )
            
            # Vérifier que l'activité n'a pas encore eu lieu
            if registration.activity.date < timezone.now():
                return Response({'error': 'Impossible d\'annuler une inscription pour une activité passée'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            registration.status = 'cancelled'
            registration.save()
            
            return Response({'message': 'Inscription annulée'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserActivityView(APIView):
    """Vue pour les activités de l'utilisateur"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les activités de l'utilisateur (inscrites et organisées)"""
        try:
            # Activités inscrites
            registered_activities = ActivityRegistration.objects.filter(
                user=request.user,
                status='confirmed'
            ).select_related('activity')
            
            # Activités organisées
            organized_activities = Activity.objects.filter(
                organizer=request.user,
                is_active=True
            )
            
            data = {
                'registered_activities': [{
                    'registration_id': reg.id,
                    'registration_date': reg.registration_date.isoformat(),
                    'notes': reg.notes,
                    'activity': ActivitySerializer(reg.activity, context={'request': request}).data
                } for reg in registered_activities],
                'organized_activities': ActivitySerializer(organized_activities, many=True, context={'request': request}).data
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES NOTIFICATIONS =====

class NotificationView(APIView):
    """Vue pour gérer les notifications"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les notifications de l'utilisateur"""
        try:
            notifications = Notification.objects.filter(user=request.user)
            serializer = NotificationSerializer(notifications, many=True)
            
            # Compter les notifications non lues
            unread_count = notifications.filter(is_read=False).count()
            
            return Response({
                'notifications': serializer.data,
                'unread_count': unread_count
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, notification_id):
        """Marquer une notification comme lue"""
        try:
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.mark_as_read()
            
            return Response({'message': 'Notification marquée comme lue'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NotificationMarkAllReadView(APIView):
    """Vue pour marquer toutes les notifications comme lues"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        """Marquer toutes les notifications comme lues"""
        try:
            updated = Notification.objects.filter(
                user=request.user, 
                is_read=False
            ).update(
                is_read=True, 
                read_at=timezone.now()
            )
            
            return Response({
                'message': f'{updated} notifications marquées comme lues'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ===== VUES TABLEAU DE BORD =====

class DashboardView(APIView):
    """Vue pour le tableau de bord utilisateur"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupérer les données du tableau de bord"""
        try:
            user = request.user
            
            # Statistiques utilisateur (créer si n'existe pas)
            stats, created = UserStatistics.objects.get_or_create(user=user)
            
            # Activités à venir
            upcoming_activities = Activity.objects.filter(
                registrations__user=user,
                registrations__status='confirmed',
                date__gte=timezone.now(),
                is_active=True
            ).distinct()[:5]
            
            # Messages récents
            recent_messages = Message.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).order_by('-created_at')[:10]
            
            # Demandes d'amis en attente
            pending_requests = Contact.objects.filter(
                contact=user,
                status='pending'
            )[:5]
            
            # Notifications récentes
            recent_notifications = Notification.objects.filter(
                user=user
            )[:10]
            
            data = {
                'user_stats': UserStatisticsSerializer(stats).data,
                'upcoming_activities': ActivitySerializer(upcoming_activities, many=True, context={'request': request}).data,
                'recent_messages': MessageSerializer(recent_messages, many=True).data,
                'pending_requests': ContactSerializer(pending_requests, many=True).data,
                'recent_notifications': NotificationSerializer(recent_notifications, many=True).data,
                'unread_messages_count': Message.objects.filter(receiver=user, is_read=False).count(),
                'unread_notifications_count': Notification.objects.filter(user=user, is_read=False).count(),
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
