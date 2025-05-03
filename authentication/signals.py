from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a profile for each new user, but only if one doesn't already exist.
    """
    if created:
        # Only create a new profile if this is a new user
        Profile.objects.get_or_create(owner=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the profile when the user is saved
    """
    # Get the profile if it exists (or create one if it doesn't)
    profile, created = Profile.objects.get_or_create(owner=instance)
    if not created:
        # If the profile already existed, just save it
        profile.save()


@receiver(user_logged_in)
def update_last_login_display(sender, user, request, **kwargs):
    """
    Signal handler to update the last_login_display field when a user logs in
    """
    # Use filter().first() instead of get() to prevent MultipleObjectsReturned error
    profile = Profile.objects.filter(owner=user).first()
    if profile:
        profile.last_login_display = timezone.now()
        profile.save()
    else:
        # Create a profile if it doesn't exist
        Profile.objects.create(owner=user, last_login_display=timezone.now()) 