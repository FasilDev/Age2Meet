from rest_framework import serializers
from .models import User, UserProfile, Contact, Message, Event, Review, TutorialVideo

class UserSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil utilisateur"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location', 'interests', 'status', 'profile_picture', 'is_verified', 'created_at']
        read_only_fields = ['created_at', 'is_verified']

class ContactSerializer(serializers.ModelSerializer):
    """Serializer pour les contacts"""
    user = UserSerializer(read_only=True)
    contact = UserSerializer(read_only=True)
    
    class Meta:
        model = Contact
        fields = ['id', 'user', 'contact', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer pour les messages"""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    """Serializer pour les événements"""
    user = UserSerializer(read_only=True)
    attendees = UserSerializer(many=True, read_only=True)
    attendees_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'user', 'title', 'description', 'event_type', 'location', 
                 'start_date', 'end_date', 'attendees', 'attendees_count', 'is_public', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_attendees_count(self, obj):
        return obj.attendees.count()

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer pour les avis"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'is_approved', 'created_at']
        read_only_fields = ['id', 'is_approved', 'created_at']

class TutorialVideoSerializer(serializers.ModelSerializer):
    """Serializer pour les vidéos tutoriels"""
    class Meta:
        model = TutorialVideo
        fields = ['id', 'title', 'description', 'video_url', 'thumbnail', 'order', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription utilisateur"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'date_of_birth', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer pour la connexion utilisateur"""
    email = serializers.EmailField()
    password = serializers.CharField()

class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un message"""
    receiver_id = serializers.IntegerField()
    
    class Meta:
        model = Message
        fields = ['receiver_id', 'content']
    
    def create(self, validated_data):
        receiver_id = validated_data.pop('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        validated_data['receiver'] = receiver
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

class EventCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un événement"""
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'location', 'start_date', 'end_date', 'is_public']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ContactCreateSerializer(serializers.Serializer):
    """Serializer pour créer une demande de contact"""
    contact_id = serializers.IntegerField()
    
    def create(self, validated_data):
        contact_id = validated_data['contact_id']
        contact_user = User.objects.get(id=contact_id)
        user = self.context['request'].user
        
        return Contact.objects.create(
            user=user,
            contact=contact_user,
            status='pending'
        )

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour le profil"""
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone = serializers.CharField(source='user.phone')
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'bio', 'location', 'interests', 'status']
    
    def update(self, instance, validated_data):
        # Mettre à jour les champs utilisateur
        user_data = validated_data.pop('user', {})
        for field, value in user_data.items():
            setattr(instance.user, field, value)
        instance.user.save()
        
        # Mettre à jour les champs profil
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        
        return instance 