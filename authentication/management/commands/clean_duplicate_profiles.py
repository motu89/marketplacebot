from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import Profile


class Command(BaseCommand):
    help = 'Cleans up duplicate Profile objects by keeping only the most recent one for each user'

    def handle(self, *args, **options):
        # Get all users
        users = User.objects.all()
        fixed_count = 0

        for user in users:
            # Get all profiles for this user
            profiles = Profile.objects.filter(owner=user).order_by('-created_at')
            
            # If more than one profile exists, keep only the newest one
            if profiles.count() > 1:
                self.stdout.write(f"Found {profiles.count()} profiles for user {user.username}")
                # Keep the first one (newest by created_at) and delete the rest
                primary_profile = profiles.first()
                for profile in profiles[1:]:
                    self.stdout.write(f"Deleting duplicate profile ID {profile.id} for user {user.username}")
                    profile.delete()
                fixed_count += 1
        
        if fixed_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully cleaned up profiles for {fixed_count} users'))
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate profiles found')) 