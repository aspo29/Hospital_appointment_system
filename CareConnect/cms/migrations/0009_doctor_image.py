# Generated by Django 5.0.6 on 2024-06-12 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_alter_speciality_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='doctor_images/'),
        ),
    ]
