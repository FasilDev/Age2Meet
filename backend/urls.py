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
    
    # NOUVELLE ROUTE pour l'upload de photo (si solution 2)
    path('profile/upload-picture/', views.ProfilePictureUploadView.as_view(), name='profile_picture_upload'),
    
    # ===== MESSAGERIE =====
    path('messages/', views.MessageView.as_view(), name='messages'),
    
    # ===== CONTACTS =====
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('contacts/<int:contact_id>/action/', views.ContactActionView.as_view(), name='contact_action'),
    path('contacts/<int:contact_id>/', views.ContactDeleteView.as_view(), name='contact_delete'),
    
    # ===== AGENDA =====
    path('events/', views.EventView.as_view(), name='events'),
    
    # ===== ACTIVITÉS =====
    path('activities/', views.ActivityView.as_view(), name='activities'),
    path('activities/<int:activity_id>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('activities/register/', views.ActivityRegistrationView.as_view(), name='activity_register'),
    path('activities/registration/<int:registration_id>/', views.ActivityRegistrationView.as_view(), name='activity_registration_cancel'),
    path('user/activities/', views.UserActivityView.as_view(), name='user_activities'),
    
    # ===== NOTIFICATIONS =====
    path('notifications/', views.NotificationView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/read/', views.NotificationView.as_view(), name='notification_read'),
    path('notifications/mark-all-read/', views.NotificationMarkAllReadView.as_view(), name='notifications_mark_all_read'),
    
    # ===== TABLEAU DE BORD =====
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # ===== ACCUEIL =====
    path('home/', views.HomeView.as_view(), name='home'),
    
    # ===== AVIS =====
    path('reviews/', views.ReviewView.as_view(), name='reviews'),
    
    # ===== DOCUMENTATION =====
    path('docs/', APIDocsView.as_view(), name='api_docs'),
] 
