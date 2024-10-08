# Generated by Django 5.0.6 on 2024-07-05 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0018_remove_appointment_doctor_remove_appointment_patient_and_more'),
        ('doctors', '0001_initial'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('symptom_description', models.TextField(blank=True, default='')),
                ('appointment_date', models.DateField(null=True)),
                ('appointment_time', models.IntegerField(choices=[(0, '09:00 – 10:00'), (1, '10:00 – 11:00'), (2, '11:00 – 12:00'), (3, '12:00 – 13:00'), (4, '13:00 – 14:00'), (5, '14:00 – 15:00'), (6, '15:00 – 16:00'), (7, '16:00 – 17:00'), (8, '17:00 – 18:00')], null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
                ('specialty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.speciality')),
            ],
        ),
    ]
