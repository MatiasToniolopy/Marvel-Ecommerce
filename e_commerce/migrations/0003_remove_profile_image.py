# Generated by Django 4.0 on 2022-04-15 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0002_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
