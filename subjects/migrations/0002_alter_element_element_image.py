# Generated by Django 5.0.7 on 2024-07-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='element_image',
            field=models.ImageField(upload_to=''),
        ),
    ]
