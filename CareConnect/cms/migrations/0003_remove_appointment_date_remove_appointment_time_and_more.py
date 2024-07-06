# Generated by Django 5.0.6 on 2024-06-11 18:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_token_appointment_token_patient_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='token',
        ),
        migrations.RemoveField(
            model_name='token',
            name='token_count',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='booked_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='symptom_description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='available_tokens',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.token'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(max_length=70),
        ),
    ]
