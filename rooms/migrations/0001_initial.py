# Generated by Django 5.0.7 on 2024-07-19 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('element_id', models.AutoField(primary_key=True, serialize=False)),
                ('element_name', models.CharField(max_length=255)),
                ('element_image', models.CharField(max_length=255)),
                ('num_won', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('max_people', models.IntegerField()),
                ('current_people', models.IntegerField(default=1)),
                ('is_started', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=255)),
                ('num_used', models.IntegerField(default=0)),
            ],
        ),
    ]
