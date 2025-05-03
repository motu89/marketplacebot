import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FBBot.settings')
django.setup()

from django.contrib.auth.models import User

# Check if user already exists
if User.objects.filter(username='motu').exists():
    user = User.objects.get(username='motu')
    user.set_password('motu')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("User 'motu' already exists. Password has been updated.")
else:
    # Create new superuser
    User.objects.create_superuser('motu', 'motu@example.com', 'motu')
    print("Superuser 'motu' has been created successfully.") 