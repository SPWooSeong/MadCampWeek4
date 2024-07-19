from django.db import models

# Create your models here.
class User(models.Model):
    google_account = models.CharField(max_length=100, null=False, primary_key=True)
    nickname = models.CharField(max_length=100, null=False)
    profile_image_url = models.URLField(null=False)