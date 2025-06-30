from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Modèle utilisateur personnalisé pour le site de rencontres"""
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class UserProfile(models.Model):
    """Profil utilisateur avec informations détaillées"""
    STATUS_CHOICES = [
        ('online', 'En ligne'),
        ('away', 'Absent'),
        ('busy', 'Ne pas déranger'),
        ('offline', 'Hors ligne'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    interests = models.TextField(max_length=300, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"

class Contact(models.Model):
    """Modèle pour gérer les contacts/amis"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('declined', 'Refusé'),
        ('blocked', 'Bloqué'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'contact')
    
    def __str__(self):
        return f"{self.user.username} -> {self.contact.username} ({self.status})"

class Message(models.Model):
    """Modèle pour la messagerie"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message de {self.sender.username} à {self.receiver.username}"

class Event(models.Model):
    """Modèle pour l'agenda/événements"""
    EVENT_TYPE_CHOICES = [
        ('personal', 'Personnel'),
        ('public', 'Public'),
        ('meetup', 'Rencontre'),
        ('activity', 'Activité'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='personal')
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendees = models.ManyToManyField(User, blank=True, related_name='attending_events')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%d/%m/%Y')}"

class Review(models.Model):
    """Modèle pour les avis utilisateurs du site"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 à 5 étoiles
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Avis de {self.user.username} - {self.rating}/5"

class TutorialVideo(models.Model):
    """Modèle pour les vidéos tutoriels"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='tutorial_thumbnails/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title

class Activity(models.Model):
    """Modèle pour les activités Age2meet (cuisine, balade, etc.)"""
    ACTIVITY_TYPE_CHOICES = [
        ('cuisine', 'Atelier Cuisine'),
        ('balade', 'Balade Nature'),
        ('musee', 'Visite Musée'),
        ('lecture', 'Club Lecture'),
        ('jardinage', 'Jardinage'),
        ('sport', 'Sport Doux'),
        ('art', 'Atelier Art'),
        ('jeux', 'Jeux de Société'),
        ('cinema', 'Cinéma'),
        ('theatre', 'Théâtre'),
        ('danse', 'Danse'),
        ('cafe', 'Café Rencontre'),
        ('autre', 'Autre'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    max_participants = models.IntegerField(default=10)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='facile')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_activities')
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True)
    requirements = models.TextField(blank=True, help_text="Matériel nécessaire, prérequis, etc.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Activities"
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d/%m/%Y')}"
    
    @property
    def participants_count(self):
        return self.registrations.filter(status='confirmed').count()
    
    @property
    def is_full(self):
        return self.participants_count >= self.max_participants
    
    @property
    def available_spots(self):
        return self.max_participants - self.participants_count

class ActivityRegistration(models.Model):
    """Modèle pour les inscriptions aux activités"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
        ('no_show', 'Absent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_registrations')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Notes personnelles ou besoins spéciaux")
    rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(blank=True, help_text="Commentaire après l'activité")
    
    class Meta:
        unique_together = ('user', 'activity')
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.user.username} -> {self.activity.title} ({self.status})"

class Notification(models.Model):
    """Modèle pour les notifications utilisateurs"""
    NOTIFICATION_TYPE_CHOICES = [
        ('message', 'Nouveau message'),
        ('contact_request', 'Demande d\'ami'),
        ('contact_accepted', 'Ami accepté'),
        ('activity_reminder', 'Rappel activité'),
        ('activity_cancelled', 'Activité annulée'),
        ('activity_updated', 'Activité modifiée'),
        ('event_reminder', 'Rappel événement'),
        ('system', 'Notification système'),
        ('welcome', 'Bienvenue'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=500, blank=True, help_text="URL pour action liée à la notification")
    related_object_id = models.IntegerField(null=True, blank=True, help_text="ID de l'objet lié (message, activité, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification pour {self.user.username}: {self.title}"
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

class UserStatistics(models.Model):
    """Modèle pour les statistiques utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    activities_participated = models.IntegerField(default=0)
    events_created = models.IntegerField(default=0)
    messages_sent = models.IntegerField(default=0)
    friends_count = models.IntegerField(default=0)
    profile_views = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stats de {self.user.username}"
