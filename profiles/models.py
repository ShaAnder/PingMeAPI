from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Profile(models.Model):
  STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('afk', 'Away'),
        ('dnd', 'Do Not Disturb'),
    ]
  owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  status_mode = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='online'
    )
  status_text = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
  name = models.CharField(max_length=255, blank=True)
  location = models.CharField(max_length=100, blank=True, null=True)
  content = models.TextField(blank=True)
  image = CloudinaryField(
        'image',  
        folder='Avatars',  
        default='default_profile_uxlg3a.jpg'
      )

  
  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f"{self.owner}'s profile"
  
def create_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(owner=instance)
  
post_save.connect(create_profile, sender=User)