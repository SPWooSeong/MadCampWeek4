from django.db import models

# Create your models here.
class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True,null=False)
    subject_name = models.CharField(max_length=255, blank=False,null=False)
    num_used = models.IntegerField(default=0,null=False)

    def __str__(self):
        return str(self.subject_id)

class Element(models.Model):
    element_id = models.AutoField(primary_key=True,null=False)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    element_name = models.CharField(max_length=255, blank=False,null=False)
    element_image = models.ImageField(upload_to="", null=False)
    num_won = models.IntegerField(default=0,null=False)

    def __str__(self):
        return str(self.element_id)
