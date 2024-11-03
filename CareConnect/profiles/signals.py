from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save the profile whenever the User object is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Signal to handle updates in the Profile model
@receiver(post_save, sender=Profile)
def profile_picture_updated(sender, instance, **kwargs):
    if instance.profile_picture:
        # Add any logic you want to perform when a profile picture is updated
        # For example, you could log the change or perform other actions
        print(f"Profile picture updated for user: {instance.user.username}")