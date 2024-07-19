from django.db import models

from rooms.models import Room

# Create your models here.
class User(models.Model):
    google_account = models.CharField(max_length=100, null=False, primary_key=True, blank=False)
    nickname = models.CharField(max_length=100, null=False, blank=False)
    profile_image_url = models.URLField(null=False, blank=False)
    room_id = models.ForeignKey('rooms.Room', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nickname
    