# Generated by Django 5.0.6 on 2024-06-13 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_alter_patient_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='available_tokens',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='token_number',
        ),
    ]
