# Generated by Django 5.0.6 on 2024-06-12 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_speciality'),
    ]

    operations = [
        migrations.AddField(
            model_name='speciality',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='specialty_images/'),
        ),
    ]
