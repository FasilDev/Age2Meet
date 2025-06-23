from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Contact, Message, Event, Review, TutorialVideo

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

# Enregistrer le modèle User personnalisé
admin.site.register(User, UserAdmin)

# Personnaliser l'en-tête de l'admin
admin.site.site_header = "Age2Meet - Administration"
admin.site.site_title = "Age2Meet Admin"
admin.site.index_title = "Bienvenue dans l'administration Age2Meet"
