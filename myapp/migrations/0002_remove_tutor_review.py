# Generated by Django 4.1.6 on 2023-04-16 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='review',
        ),
    ]
