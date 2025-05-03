import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FBBot.settings')
django.setup()

from django.contrib.auth.models import User

# Update the password for user 'motu'
try:
    user = User.objects.get(username='motu')
    user.set_password('motu4671')
    user.save()
    print("Password for user 'motu' has been updated to 'motu4671'.")
except User.DoesNotExist:
    print("User 'motu' does not exist. Please create the user first.") 