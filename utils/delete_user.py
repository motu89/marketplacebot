import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FBBot.settings')
django.setup()

from django.contrib.auth.models import User

# Delete the 'adnanrafique' user account
try:
    user = User.objects.get(username='adnanrafique')
    username = user.username  # Store for confirmation message
    user.delete()
    print(f"User '{username}' has been successfully deleted.")
except User.DoesNotExist:
    print("User 'adnanrafique' does not exist.")

# Print all remaining superusers for confirmation
superusers = User.objects.filter(is_superuser=True)
print("\nRemaining superusers:")
for user in superusers:
    print(f"- {user.username} ({user.email})") 