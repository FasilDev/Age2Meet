print("=== TOUTES LES RELATIONS ===")
from backend.models import Contact
for contact in Contact.objects.all():
    print(f"{contact.id}: {contact.user.username} -> {contact.contact.username} ({contact.status})")
