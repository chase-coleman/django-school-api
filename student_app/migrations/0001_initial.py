# Generated by Django 5.1.7 on 2025-03-27 01:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(default='Unknown', unique=True)),
                ('professor', models.CharField(default='Mr. Cahan')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[A-Z][a-z]+ [A-Z]\\. [A-Z][a-z]+$', message='Name must be in the format "First Middle Initial. Last"')])),
                ('student_email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9._%+-]+@school\\.com$', message='Invalid school email format. Please use an email ending with "@school.com".')])),
                ('personal_email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('locker_number', models.IntegerField(default=110, unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)])),
                ('locker_combination', models.CharField(blank=True, default='12-12-12', max_length=20, validators=[django.core.validators.RegexValidator('^\\d{2}-\\d{2}-\\d{2}$', message='Combination must be in the format "12-12-12"')])),
                ('good_student', models.BooleanField(default=True)),
                ('subjects', models.ManyToManyField(related_name='students', to='student_app.subject')),
            ],
        ),
    ]
