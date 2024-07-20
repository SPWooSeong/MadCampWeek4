from django.db import models



class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True,null=False)
    subject_name = models.CharField(max_length=255, blank=False,null=False)
    num_used = models.IntegerField(default=0,null=False)

    def __str__(self):
        return self.subject_id
    
class Room(models.Model):
    room_id = models.AutoField(primary_key=True,null=False)
    google_account = models.OneToOneField('users.User', on_delete=models.CASCADE)
    room_title = models.CharField(max_length=255, blank=False,null=False)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    max_people = models.IntegerField(null=False)
    current_people = models.IntegerField(default=1,null=False)
    is_started = models.BooleanField(default=False,null=False)

    def __str__(self):
        return str(self.room_id)
    
class Element(models.Model):
    element_id = models.AutoField(primary_key=True,null=False)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    element_name = models.CharField(max_length=255, blank=False,null=False)
    element_image = models.CharField(max_length=255, null=False)
    num_won = models.IntegerField(default=0,null=False)

    def __str__(self):
        return self.element_id