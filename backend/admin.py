from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Contact, Message, Event, Review, TutorialVideo, Activity, ActivityRegistration, Notification, UserStatistics

# ===== ADMINISTRATION UTILISATEUR =====

class UserProfileInline(admin.StackedInline):
    """Inline pour le profil utilisateur"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profils'

class UserAdmin(BaseUserAdmin):
    """Administration des utilisateurs"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Champs pour la création d'utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'phone'),
        }),
    )
    
    # Champs pour la modification d'utilisateur
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('date_of_birth', 'phone')}),
    )

# ===== ADMINISTRATION PROFIL =====

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Administration des profils utilisateur"""
    list_display = ('user', 'status', 'location', 'is_verified', 'created_at')
    list_filter = ('status', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'location')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'bio', 'location', 'interests')
        }),
        ('Statut et paramètres', {
            'fields': ('status', 'is_verified', 'profile_picture')
        }),
    )

# ===== ADMINISTRATION CONTACTS =====

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Administration des contacts"""
    list_display = ('user', 'contact', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'contact__username')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Relation', {
            'fields': ('user', 'contact', 'status')
        }),
    )

# ===== ADMINISTRATION MESSAGES =====

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Administration des messages"""
    list_display = ('sender', 'receiver', 'content_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'content')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Message', {
            'fields': ('sender', 'receiver', 'content', 'is_read')
        }),
    )
    
    def content_preview(self, obj):
        """Aperçu du contenu du message"""
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
    content_preview.short_description = 'Aperçu du contenu'

# ===== ADMINISTRATION ÉVÉNEMENTS =====

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Administration des événements"""
    list_display = ('title', 'user', 'event_type', 'start_date', 'end_date', 'is_public', 'attendees_count')
    list_filter = ('event_type', 'is_public', 'start_date', 'created_at')
    search_fields = ('title', 'user__username', 'location', 'description')
    ordering = ('-start_date',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'description', 'user', 'event_type')
        }),
        ('Lieu et date', {
            'fields': ('location', 'start_date', 'end_date')
        }),
        ('Paramètres', {
            'fields': ('is_public', 'attendees')
        }),
    )
    
    filter_horizontal = ('attendees',)
    
    def attendees_count(self, obj):
        """Nombre de participants"""
        return obj.attendees.count()
    attendees_count.short_description = 'Participants'

# ===== ADMINISTRATION AVIS =====

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Administration des avis"""
    list_display = ('user', 'rating', 'comment_preview', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'comment')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Avis', {
            'fields': ('user', 'rating', 'comment', 'is_approved')
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def comment_preview(self, obj):
        """Aperçu du commentaire"""
        if len(obj.comment) > 50:
            return obj.comment[:50] + '...'
        return obj.comment
    comment_preview.short_description = 'Aperçu du commentaire'
    
    def approve_reviews(self, request, queryset):
        """Action pour approuver les avis"""
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} avis approuvés.')
    approve_reviews.short_description = 'Approuver les avis sélectionnés'
    
    def disapprove_reviews(self, request, queryset):
        """Action pour désapprouver les avis"""
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} avis désapprouvés.')
    disapprove_reviews.short_description = 'Désapprouver les avis sélectionnés'

# ===== ADMINISTRATION VIDÉOS TUTORIELS =====

@admin.register(TutorialVideo)
class TutorialVideoAdmin(admin.ModelAdmin):
    """Administration des vidéos tutoriels"""
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order', 'created_at')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'description', 'video_url', 'thumbnail')
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active')
        }),
    )

# ===== ADMINISTRATION ACTIVITÉS =====

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Administration des activités Age2meet"""
    list_display = ('title', 'activity_type', 'organizer', 'date', 'location', 'participants_count', 'max_participants', 'is_active')
    list_filter = ('activity_type', 'difficulty', 'is_active', 'date', 'created_at')
    search_fields = ('title', 'description', 'location', 'organizer__username')
    ordering = ('-date',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'description', 'activity_type', 'organizer')
        }),
        ('Lieu et date', {
            'fields': ('location', 'address', 'date', 'end_date')
        }),
        ('Paramètres', {
            'fields': ('max_participants', 'price', 'difficulty', 'requirements', 'image')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('participants_count', 'created_at', 'updated_at')
    
    def participants_count(self, obj):
        """Nombre de participants inscrits"""
        return obj.participants_count
    participants_count.short_description = 'Participants inscrits'

class ActivityRegistrationInline(admin.TabularInline):
    """Inline pour les inscriptions aux activités"""
    model = ActivityRegistration
    extra = 0
    readonly_fields = ('registration_date',)
    fields = ('user', 'status', 'registration_date', 'notes', 'rating')

@admin.register(ActivityRegistration)
class ActivityRegistrationAdmin(admin.ModelAdmin):
    """Administration des inscriptions aux activités"""
    list_display = ('user', 'activity', 'status', 'registration_date', 'rating')
    list_filter = ('status', 'registration_date', 'activity__activity_type')
    search_fields = ('user__username', 'activity__title')
    ordering = ('-registration_date',)
    
    fieldsets = (
        ('Inscription', {
            'fields': ('user', 'activity', 'status', 'notes')
        }),
        ('Évaluation (après activité)', {
            'fields': ('rating', 'feedback')
        }),
    )
    
    readonly_fields = ('registration_date',)

# ===== ADMINISTRATION NOTIFICATIONS =====

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Administration des notifications"""
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Notification', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Paramètres', {
            'fields': ('is_read', 'action_url', 'related_object_id')
        }),
    )
    
    readonly_fields = ('created_at', 'read_at')
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Action pour marquer comme lues"""
        from django.utils import timezone
        queryset.update(is_read=True, read_at=timezone.now())
        self.message_user(request, f'{queryset.count()} notifications marquées comme lues.')
    mark_as_read.short_description = 'Marquer comme lues'
    
    def mark_as_unread(self, request, queryset):
        """Action pour marquer comme non lues"""
        queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{queryset.count()} notifications marquées comme non lues.')
    mark_as_unread.short_description = 'Marquer comme non lues'

# ===== ADMINISTRATION STATISTIQUES =====

@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    """Administration des statistiques utilisateur"""
    list_display = ('user', 'activities_participated', 'events_created', 'messages_sent', 'friends_count', 'last_activity')
    list_filter = ('join_date', 'last_activity')
    search_fields = ('user__username', 'user__email')
    ordering = ('-last_activity',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Statistiques d\'activité', {
            'fields': ('activities_participated', 'events_created', 'messages_sent', 'friends_count', 'profile_views')
        }),
        ('Dates', {
            'fields': ('join_date', 'last_activity')
        }),
    )
    
    readonly_fields = ('join_date', 'last_activity')

# Enregistrer le modèle User personnalisé
admin.site.register(User, UserAdmin)

# Personnaliser l'en-tête de l'admin
admin.site.site_header = "Age2Meet - Administration"
admin.site.site_title = "Age2Meet Admin"
admin.site.index_title = "Bienvenue dans l'administration Age2Meet"
