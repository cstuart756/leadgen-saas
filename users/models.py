
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class UserProfile(models.Model):
	TIER_CHOICES = [
		('basic', 'Basic'),
		('pro', 'Pro'),
		('premium', 'Premium'),
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='basic')

	def __str__(self):
		return f"{self.user.username} ({self.tier})"
