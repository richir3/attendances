# Generated by Django 5.1.3 on 2024-12-09 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0004_attender_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attender',
            name='last_login',
        ),
    ]