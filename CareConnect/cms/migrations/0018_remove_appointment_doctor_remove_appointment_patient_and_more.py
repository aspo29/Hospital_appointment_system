# Generated by Django 5.0.6 on 2024-07-05 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_alter_appointment_appointment_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='profession',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
    ]
