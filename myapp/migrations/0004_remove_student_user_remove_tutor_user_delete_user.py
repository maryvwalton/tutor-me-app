# Generated by Django 4.1.6 on 2023-03-17 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_tutor_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
