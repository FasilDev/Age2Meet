from django.urls import path, include
from . import views  # Version propre sans erreurs Pylance
from .api_docs import APIDocsView

app_name = 'backend'

urlpatterns = [
    # ===== AUTHENTIFICATION =====
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    
    # ===== PROFIL =====
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # ===== MESSAGERIE =====
    path('messages/', views.MessageView.as_view(), name='messages'),
    
    # ===== CONTACTS =====
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('contacts/<int:contact_id>/action/', views.ContactActionView.as_view(), name='contact_action'),
    
    # ===== AGENDA =====
    path('events/', views.EventView.as_view(), name='events'),
    
    # ===== ACCUEIL =====
    path('home/', views.HomeView.as_view(), name='home'),
    
    # ===== AVIS =====
    path('reviews/', views.ReviewView.as_view(), name='reviews'),
    
    # ===== DOCUMENTATION =====
    path('docs/', APIDocsView.as_view(), name='api_docs'),
] 