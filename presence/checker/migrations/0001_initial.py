# Generated by Django 5.1.3 on 2024-11-29 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('surname', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(error_messages={'invalid': 'Enter a valid email address.', 'unique': 'This email is already in use.'}, max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('location', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checker.attender')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checker.event')),
            ],
        ),
        migrations.AddField(
            model_name='attender',
            name='events',
            field=models.ManyToManyField(through='checker.Attendance', to='checker.event'),
        ),
    ]
