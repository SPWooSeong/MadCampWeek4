from django.db import models

# Create your models here.
class User(models.Model):
    google_account = models.CharField(max_length=100, null=False, primary_key=True, blank=False)
    nickname = models.CharField(max_length=100, null=False, blank=False)
    profile_image_url = models.URLField(null=False, blank=False)
    current_room_id = models.IntegerField(null=True, default=None)
    
    def __str__(self):
        return self.nickname
    