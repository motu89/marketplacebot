from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import Profile


class Command(BaseCommand):
    help = 'Updates Profile.last_login_display values with User.last_login for existing profiles'

    def handle(self, *args, **options):
        profiles = Profile.objects.all()
        updated_count = 0

        for profile in profiles:
            if profile.owner and profile.owner.last_login:
                profile.last_login_display = profile.owner.last_login
                profile.save()
                updated_count += 1
                self.stdout.write(f"Updated last_login_display for user: {profile.owner.username}")
        
        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated last_login_display for {updated_count} profiles'))
        else:
            self.stdout.write(self.style.SUCCESS('No profiles needed updating')) 