# Generated by Django 4.0 on 2022-04-15 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='', upload_to='', verbose_name='imagen'),
        ),
    ]
