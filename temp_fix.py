from backend.models import Contact, User
marie = User.objects.get(username="marie.dubois")
jean = User.objects.get(username="JeanPormanove")
relation = Contact.objects.get(user=marie, contact=jean)
print(f"Avant: {relation.status}")
relation.status = "pending"
relation.save()
print(f"Après: {relation.status}")
