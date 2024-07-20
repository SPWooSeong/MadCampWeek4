from django.db import models

from subjects.models import Subject

class Room(models.Model):
    room_id = models.AutoField(primary_key=True,null=False)
    google_account = models.OneToOneField('users.User', on_delete=models.CASCADE)
    room_title = models.CharField(max_length=255, blank=False,null=False, default='')
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    max_people = models.IntegerField(null=False)
    current_people = models.IntegerField(default=1,null=False)
    is_started = models.BooleanField(default=False,null=False)

    def __str__(self):
        return str(self.room_id)
    
