# Generated by Django 5.0.6 on 2024-06-12 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_remove_appointment_token_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discounted_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.PositiveIntegerField()),
            ],
        ),
    ]
