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

from .models import User, UserProfile, Contact, Message, Event, Review, TutorialVideo

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
                
                # Mettre à jour le statut en ligne
                profile = user.profile
                profile.status = 'online'
                profile.save()
                
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
            # Mettre à jour le statut hors ligne
            profile = request.user.profile
            profile.status = 'offline'
            profile.save()
            
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
            profile.save()
            
            return Response({'message': 'Profil mis à jour avec succès'}, 
                          status=status.HTTP_200_OK)
            
        except Exception as e:
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
            
            # Demandes en attente
            pending_requests = Contact.objects.filter(
                contact=request.user,
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
                    'status': friend.profile.status,
                    'profile_picture': friend.profile.profile_picture.url if friend.profile.profile_picture else None,
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
            
            return Response({
                'contacts': contacts_data,
                'pending_requests': requests_data
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
            
            # Vérifier si la relation existe déjà
            existing = Contact.objects.filter(
                Q(user=request.user, contact=contact_user) |
                Q(user=contact_user, contact=request.user)
            ).exists()
            
            if existing:
                return Response({'error': 'Relation déjà existante'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
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